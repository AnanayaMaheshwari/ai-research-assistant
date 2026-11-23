from sqlalchemy.orm import Session
from database.models import ResearchRecord

def create_research(db: Session, payload: dict):
    record = ResearchRecord(
        topic=payload["topic"],
        mode=payload.get("mode", "sequential"),
        status="completed",
        report=payload.get("report", ""),
        report_path=payload.get("report_path"),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def list_research(db: Session, limit: int = 50):
    return db.query(ResearchRecord).order_by(ResearchRecord.created_at.desc()).limit(limit).all()

def get_research(db: Session, research_id: int):
    return db.query(ResearchRecord).filter(ResearchRecord.id == research_id).first()
