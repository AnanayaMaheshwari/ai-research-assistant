
from agents.orchestrator import (
    run_research,
    run_research_stream,
)


def conduct_research(
    topic: str,
    mode: str = "sequential",
    conversation_history: list = None
):
    return run_research(
        topic=topic,
        mode=mode,
        conversation_history=conversation_history or [],
        save_files=True
    )


async def conduct_research_stream(
    topic: str,
    mode: str = "sequential",
    conversation_history: list = None
):
    async for event in run_research_stream(
        topic=topic,
        mode=mode,
        conversation_history=conversation_history or [],
        save_files=True
    ):
        yield event
