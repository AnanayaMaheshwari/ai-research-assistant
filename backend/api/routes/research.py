
import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from backend.schemas.research import ResearchRequest
from backend.schemas.response import ResearchResponse
from database.database import get_db
from database.repositories import create_research
from backend.services.research_service import (
    conduct_research,
    conduct_research_stream,
)
from memory.session_manager import SessionManager


router = APIRouter(tags=["research"])
session_manager = SessionManager()


def prepare_conversation(session_id, topic):
    """
    Retrieve previous conversation and save the
    current user message before starting research.
    """

    if not session_id:
        return []

    if not session_manager.get(session_id):
        raise HTTPException(
            status_code=404,
            detail="Research session not found"
        )

    context = session_manager.get_context(session_id)

    session_manager.add_message(
        session_id=session_id,
        role="user",
        content=topic
    )

    context.append({
        "role": "user",
        "content": topic
    })

    return context


@router.post(
    "/research",
    response_model=ResearchResponse
)
def research(
    request: ResearchRequest,
    db: Session = Depends(get_db)
):
    try:
        session_id = request.session_id

        conversation_history = prepare_conversation(
            session_id,
            request.topic
        )

        result = conduct_research(
            topic=request.topic,
            mode=request.mode,
            conversation_history=conversation_history
        )

        record = create_research(db, result)

        if session_id:
            session_manager.add_message(
                session_id=session_id,
                role="assistant",
                content=record.report,
                research_id=record.id
            )

        return ResearchResponse(
            id=record.id,
            topic=record.topic,
            mode=record.mode,
            report=record.report,
            report_path=record.report_path,
            created_at=record.created_at.isoformat(),
            session_id=session_id,
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Research failed: {exc}"
        )


@router.post("/research/stream")
async def research_stream(
    request: ResearchRequest,
    db: Session = Depends(get_db)
):
    session_id = request.session_id

    conversation_history = prepare_conversation(
        session_id,
        request.topic
    )

    async def event_generator():
        try:
            async for event in conduct_research_stream(
                topic=request.topic,
                mode=request.mode,
                conversation_history=conversation_history
            ):

                if event["type"] == "finished":
                    result = event["result"]

                    record = create_research(db, result)

                    if session_id:
                        session_manager.add_message(
                            session_id=session_id,
                            role="assistant",
                            content=record.report,
                            research_id=record.id
                        )

                    payload = {
                        "type": "complete",
                        "result": {
                            "id": record.id,
                            "topic": record.topic,
                            "mode": record.mode,
                            "report": record.report,
                            "report_path": record.report_path,
                            "created_at": record.created_at.isoformat(),
                            "session_id": session_id,
                        },
                    }

                else:
                    payload = event

                yield (
                    f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
                )

        except Exception as exc:
            yield (
                "data: "
                + json.dumps({
                    "type": "error",
                    "message": str(exc)
                }, ensure_ascii=False)
                + "\n\n"
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
