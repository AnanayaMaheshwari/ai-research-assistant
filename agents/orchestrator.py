
import asyncio

from agents.planner import create_planner_agent
from agents.researcher import create_researcher_agent
from agents.analyst import create_analyst_agent
from agents.fact_checker import create_fact_checker_agent
from agents.report_writer import create_report_writer_agent
from tools.report_generator import save_report


VALID_MODES = {
    "sequential",
    "agents_as_tools",
    "graph",
    "swarm",
}


def _text(result):
    if result is None:
        return ""

    return str(result).strip()


def _validate_output(value, stage):
    if not value or not value.strip():
        raise RuntimeError(
            f"{stage} returned an empty response. "
            "The next agent was not executed."
        )

    return value


def _build_context(conversation_history):
    if not conversation_history:
        return "No previous conversation is available."

    parts = []

    for message in conversation_history:
        role = message.get("role", "unknown").upper()
        content = message.get("content", "")

        if content:
            parts.append(
                f"{role}:\n{content}"
            )

    return "\n\n".join(parts)


def _build_request(topic, conversation_history):
    context = _build_context(conversation_history)

    return f"""
You are continuing a research conversation.

PREVIOUS CONVERSATION:
{context}

CURRENT USER MESSAGE:
{topic}

INSTRUCTIONS:
1. Understand the current message using the previous conversation.
2. If it is a follow-up, preserve the original research topic and
   use the earlier findings and report as context.
3. Resolve references such as "it", "this", "that", and
   "the second finding" using the conversation history.
4. If the user explicitly introduces a completely new topic,
   treat it as a new research task.
5. Do not invent missing information.
6. Clearly distinguish new findings from previously established
   information.

Complete the requested research task.
"""


def _sequential_research(topic, request_prompt):
    plan = _validate_output(
        _text(
            create_planner_agent()(
                f"""
Create a research plan for the user's current request.

{request_prompt}
"""
            )
        ),
        "Planner"
    )

    research = _validate_output(
        _text(
            create_researcher_agent()(
                f"""
Research the user's current request.

{request_prompt}

RESEARCH PLAN:
{plan}

Use web search where appropriate.
Return detailed findings with source URLs.
"""
            )
        ),
        "Researcher"
    )

    analysis = _validate_output(
        _text(
            create_analyst_agent()(
                f"""
Analyze the research findings.

ORIGINAL REQUEST AND CONTEXT:
{request_prompt}

RESEARCH PLAN:
{plan}

RESEARCH FINDINGS:
{research}

Do not invent additional evidence.
"""
            )
        ),
        "Analyst"
    )

    review = _validate_output(
        _text(
            create_fact_checker_agent()(
                f"""
Review the research findings and analysis.

ORIGINAL REQUEST AND CONTEXT:
{request_prompt}

RESEARCH FINDINGS:
{research}

ANALYSIS:
{analysis}

Identify unsupported claims and corrections.
"""
            )
        ),
        "FactChecker"
    )

    report = _validate_output(
        _text(
            create_report_writer_agent()(
                f"""
Write the final research report.

ORIGINAL REQUEST AND CONTEXT:
{request_prompt}

RESEARCH PLAN:
{plan}

RESEARCH FINDINGS:
{research}

ANALYSIS:
{analysis}

FACT-CHECKING REVIEW:
{review}

Produce a complete Markdown report.
"""
            )
        ),
        "ReportWriter"
    )

    return {
        "topic": topic,
        "mode": "sequential",
        "plan": plan,
        "research": research,
        "analysis": analysis,
        "fact_check": review,
        "report": report,
    }


def run_research(
    topic: str,
    mode: str = "sequential",
    conversation_history: list = None,
    save_files: bool = True
):
    if not topic or not topic.strip():
        raise ValueError("Research topic cannot be empty.")

    if mode not in VALID_MODES:
        raise ValueError(
            f"Invalid research mode: {mode}"
        )

    conversation_history = conversation_history or []

    request_prompt = _build_request(
        topic,
        conversation_history
    )

    if mode == "sequential":

        result = _sequential_research(
            topic,
            request_prompt
        )

    elif mode == "agents_as_tools":

        from agents.workflows.agents_as_tools import run_as_tools

        output = run_as_tools(
            topic,
            conversation_history
        )

        report = _validate_output(
            _text(output),
            "Agents-as-Tools workflow"
        )

        result = {
            "topic": topic,
            "mode": mode,
            "plan": "",
            "research": "",
            "analysis": "",
            "fact_check": "",
            "report": report
        }

    elif mode == "graph":

        from agents.workflows.research_graph import run_graph

        output = run_graph(
            topic,
            conversation_history
        )

        report = _validate_output(
            _text(output),
            "Graph workflow"
        )

        result = {
            "topic": topic,
            "mode": mode,
            "plan": "",
            "research": "",
            "analysis": "",
            "fact_check": "",
            "report": report
        }

    else:

        from agents.workflows.research_swarm import run_swarm

        output = run_swarm(
            topic,
            conversation_history
        )

        report = _validate_output(
            _text(output),
            "Swarm workflow"
        )

        result = {
            "topic": topic,
            "mode": mode,
            "plan": "",
            "research": "",
            "analysis": "",
            "fact_check": "",
            "report": report
        }

    if save_files:
        result["report_path"] = save_report(
            topic,
            result["report"]
        )

    return result


async def _stream_agent(
    agent,
    prompt: str,
    stage: str,
    stream_text: bool = False
):
    pieces = []
    final_result = None

    yield {
        "type": "stage",
        "stage": stage,
        "message": f"{stage}..."
    }

    async for event in agent.stream_async(prompt):

        if not isinstance(event, dict):
            continue

        data = event.get("data")

        if data is not None:
            chunk = str(data)
            pieces.append(chunk)

            if stream_text:
                yield {
                    "type": "token",
                    "text": chunk
                }

        if event.get("result") is not None:
            final_result = event["result"]

    output = "".join(pieces).strip()

    if not output and final_result is not None:
        output = _text(final_result)

        if stream_text and output:
            yield {
                "type": "token",
                "text": output
            }

    yield {
        "type": "stage_complete",
        "stage": stage,
        "text": output
    }


async def run_research_stream(
    topic: str,
    mode: str = "sequential",
    conversation_history: list = None,
    save_files: bool = True
):
    if not topic or not topic.strip():
        raise ValueError("Research topic cannot be empty.")

    if mode not in VALID_MODES:
        raise ValueError(
            f"Invalid research mode: {mode}"
        )

    conversation_history = conversation_history or []

    request_prompt = _build_request(
        topic,
        conversation_history
    )

    if mode != "sequential":

        labels = {
            "graph": "Running Graph workflow",
            "swarm": "Running Swarm workflow",
            "agents_as_tools": "Running Agents-as-Tools workflow"
        }

        yield {
            "type": "stage",
            "stage": labels[mode],
            "message": labels[mode] + "..."
        }

        result = await asyncio.to_thread(
            run_research,
            topic,
            mode,
            conversation_history,
            save_files
        )

        yield {
            "type": "finished",
            "result": result
        }

        return

    plan = ""
    research = ""
    analysis = ""
    review = ""

    stages = [
        (
            create_planner_agent(),
            f"""
Create a research plan.

{request_prompt}
""",
            "Planning research"
        ),
        (
            create_researcher_agent(),
            None,
            "Researching the topic"
        ),
        (
            create_analyst_agent(),
            None,
            "Analyzing findings"
        ),
        (
            create_fact_checker_agent(),
            None,
            "Fact-checking the research"
        ),
        (
            create_report_writer_agent(),
            None,
            "Writing final report"
        )
    ]

    for index, (agent, prompt, stage) in enumerate(stages):

        if index == 1:
            prompt = f"""
Research the current request.

{request_prompt}

RESEARCH PLAN:
{plan}

Return detailed findings with source URLs.
"""

        elif index == 2:
            prompt = f"""
Analyze the supplied research findings.

{request_prompt}

RESEARCH PLAN:
{plan}

RESEARCH FINDINGS:
{research}
"""

        elif index == 3:
            prompt = f"""
Review the research and analysis.

{request_prompt}

RESEARCH FINDINGS:
{research}

ANALYSIS:
{analysis}
"""

        elif index == 4:
            prompt = f"""
Write the final Markdown research report.

{request_prompt}

RESEARCH PLAN:
{plan}

RESEARCH FINDINGS:
{research}

ANALYSIS:
{analysis}

FACT-CHECKING REVIEW:
{review}
"""

        output = ""

        async for event in _stream_agent(
            agent,
            prompt,
            stage,
            stream_text=(index == 4)
        ):

            if event["type"] == "stage":
                yield event

            elif event["type"] == "token":
                yield event

            elif event["type"] == "stage_complete":
                output = event["text"]

        output = _validate_output(output, stage)

        if index == 0:
            plan = output

        elif index == 1:
            research = output

        elif index == 2:
            analysis = output

        elif index == 3:
            review = output

        elif index == 4:
            report = output

    result = {
        "topic": topic,
        "mode": mode,
        "plan": plan,
        "research": research,
        "analysis": analysis,
        "fact_check": review,
        "report": report
    }

    if save_files:
        result["report_path"] = save_report(
            topic,
            report
        )

    yield {
        "type": "finished",
        "result": result
    }
