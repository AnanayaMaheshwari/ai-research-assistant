
from pydantic import BaseModel


class ResearchResponse(BaseModel):
    id: int
    topic: str
    mode: str
    report: str
    report_path: str | None = None
    created_at: str
    session_id: str | None = None


class SessionResponse(BaseModel):
    id: str
    created_at: str
    messages: list[dict]


class SessionCreatedResponse(BaseModel):
    session_id: str
