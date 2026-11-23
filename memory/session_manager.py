
from database.database import SessionLocal
from database.models import ResearchSession, SessionMessage


class SessionManager:

    def create(self):
        db = SessionLocal()
        try:
            session = ResearchSession()
            db.add(session)
            db.commit()
            db.refresh(session)
            return session.id
        finally:
            db.close()

    def get(self, session_id):
        db = SessionLocal()
        try:
            session = (
                db.query(ResearchSession)
                .filter(ResearchSession.id == session_id)
                .first()
            )

            if not session:
                return None

            messages = sorted(
                session.messages,
                key=lambda message: message.created_at
            )

            return {
                "id": session.id,
                "created_at": session.created_at.isoformat(),
                "messages": [
                    {
                        "role": message.role,
                        "content": message.content,
                        "research_id": message.research_id,
                        "created_at": message.created_at.isoformat(),
                    }
                    for message in messages
                ],
            }
        finally:
            db.close()

    def get_context(
        self,
        session_id,
        max_messages=8,
        max_chars_per_message=6000
    ):
        session = self.get(session_id)

        if not session:
            return None

        messages = [
            message
            for message in session["messages"]
            if message.get("content")
        ]

        messages = messages[-max_messages:]

        context = []

        for message in messages:
            content = message["content"]

            if len(content) > max_chars_per_message:
                content = (
                    content[:max_chars_per_message]
                    + "\n...[Earlier content truncated]"
                )

            context.append({
                "role": message["role"],
                "content": content
            })

        return context

    def add_message(
        self,
        session_id,
        role,
        content,
        research_id=None
    ):
        db = SessionLocal()
        try:
            session = (
                db.query(ResearchSession)
                .filter(ResearchSession.id == session_id)
                .first()
            )

            if not session:
                return None

            message = SessionMessage(
                session_id=session_id,
                research_id=research_id,
                role=role,
                content=content,
            )

            db.add(message)
            db.commit()

            return True
        finally:
            db.close()
