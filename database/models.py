
from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from database.database import Base


class ResearchRecord(Base):
    __tablename__ = "research_records"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(1000), nullable=False)
    mode = Column(String(50), default="sequential")
    status = Column(String(30), default="completed")
    report = Column(Text, nullable=False)
    report_path = Column(String(2000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ResearchSession(Base):
    __tablename__ = "research_sessions"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    messages = relationship(
        "SessionMessage",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="SessionMessage.created_at",
    )


class SessionMessage(Base):
    __tablename__ = "session_messages"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    session_id = Column(
        String(36),
        ForeignKey("research_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    research_id = Column(
        Integer,
        ForeignKey("research_records.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    role = Column(String(30), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    session = relationship(
        "ResearchSession",
        back_populates="messages",
    )
