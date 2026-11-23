
from pydantic import BaseModel, Field
from typing import Literal

ResearchMode = Literal[
    "sequential",
    "graph",
    "swarm",
    "agents_as_tools",
]


class ResearchRequest(BaseModel):
    topic: str = Field(min_length=5, max_length=2000)
    mode: ResearchMode = "sequential"
    session_id: str | None = None


class SessionCreateRequest(BaseModel):
    title: str | None = None


class MessageRequest(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1)
