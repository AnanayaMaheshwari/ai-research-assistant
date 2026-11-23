
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import ResearchRecord, ResearchSession, SessionMessage
from database.repositories import list_research, get_research

router = APIRouter(tags=["history"])


@router.get("/history")
def history(limit: int = 50, db: Session = Depends(get_db)):
    records = list_research(db, min(max(limit, 1), 100))

    return [
        {
            "id": r.id,
            "topic": r.topic,
            "mode": r.mode,
            "status": r.status,
            "created_at": r.created_at.isoformat(),
        }
        for r in records
    ]


@router.get("/history/{research_id}")
def history_detail(research_id: int, db: Session = Depends(get_db)):
    record = get_research(db, research_id)

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Research record not found.",
        )

    return {
        "id": record.id,
        "topic": record.topic,
        "mode": record.mode,
        "report": record.report,
        "report_path": record.report_path,
        "created_at": record.created_at.isoformat(),
    }


@router.delete("/history/{research_id}")
def delete_research(research_id: int, db: Session = Depends(get_db)):
    record = get_research(db, research_id)

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Research record not found.",
        )

    # Find sessions containing messages for this research.
    session_ids = [
        session_id
        for (session_id,) in (
            db.query(SessionMessage.session_id)
            .filter(SessionMessage.research_id == research_id)
            .distinct()
            .all()
        )
    ]

    # Delete the messages belonging to this research.
    db.query(SessionMessage).filter(
        SessionMessage.research_id == research_id
    ).delete(synchronize_session=False)

    # Delete the research report.
    db.delete(record)
    db.flush()

    # Delete sessions that no longer contain any messages.
    for session_id in session_ids:
        remaining = (
            db.query(SessionMessage)
            .filter(SessionMessage.session_id == session_id)
            .first()
        )

        if not remaining:
            session = (
                db.query(ResearchSession)
                .filter(ResearchSession.id == session_id)
                .first()
            )

            if session:
                db.delete(session)

    db.commit()

    return {"message": "Research and its associated conversation deleted successfully."}
