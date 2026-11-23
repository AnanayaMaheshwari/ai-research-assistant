from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from backend.schemas.research import SessionCreateRequest
from backend.schemas.response import (
    SessionResponse,
    SessionCreatedResponse,
)
from database.database import SessionLocal
from database.models import (
    ResearchSession,
    SessionMessage,
    ResearchRecord,
)
from memory.session_manager import SessionManager

router = APIRouter(tags=["sessions"])
session_manager = SessionManager()


@router.post("/sessions", response_model=SessionCreatedResponse)
def create_session(request: SessionCreateRequest):
    try:
        session_id = session_manager.create()

        return SessionCreatedResponse(
            session_id=session_id
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


@router.get("/sessions")
def list_sessions():
    db: Session = SessionLocal()

    try:
        sessions = (
            db.query(ResearchSession)
            .order_by(ResearchSession.created_at.desc())
            .all()
        )

        return [
            {
                "id": session.id,
                "created_at": session.created_at.isoformat(),
                "messages": len(session.messages),
                "last_message": (
                    session.messages[-1].content[:150]
                    if session.messages
                    else "Empty session"
                ),
            }
            for session in sessions
        ]

    finally:
        db.close()


@router.get("/sessions/{session_id}", response_model=SessionResponse)
def get_session(session_id: str):
    session = session_manager.get(session_id)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    return session


@router.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    db: Session = SessionLocal()

    try:
        session = (
            db.query(ResearchSession)
            .filter(ResearchSession.id == session_id)
            .first()
        )

        if not session:
            raise HTTPException(
                status_code=404,
                detail="Research conversation not found"
            )

        # Find reports associated with this conversation.
        research_ids = {
            research_id
            for (research_id,) in (
                db.query(SessionMessage.research_id)
                .filter(
                    SessionMessage.session_id == session_id,
                    SessionMessage.research_id.isnot(None)
                )
                .distinct()
                .all()
            )
        }

        # Delete the session and its messages.
        # The relationship cascade handles message deletion.
        db.delete(session)
        db.flush()

        # Delete associated reports only if no other
        # conversation references them.
        for research_id in research_ids:
            still_referenced = (
                db.query(SessionMessage.id)
                .filter(
                    SessionMessage.research_id == research_id
                )
                .first()
            )

            if not still_referenced:
                report = (
                    db.query(ResearchRecord)
                    .filter(ResearchRecord.id == research_id)
                    .first()
                )

                if report:
                    db.delete(report)

        db.commit()

        return {
            "message": (
                "Conversation and its associated messages "
                "deleted successfully."
            )
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Could not delete conversation: {exc}"
        )

    finally:
        db.close()