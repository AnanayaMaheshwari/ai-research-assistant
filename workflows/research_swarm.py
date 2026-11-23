
from strands.multiagent import Swarm

from agents.researcher import create_researcher_agent
from agents.analyst import create_analyst_agent
from agents.fact_checker import create_fact_checker_agent
from agents.report_writer import create_report_writer_agent


def build_research_swarm():

    researcher = create_researcher_agent()
    analyst = create_analyst_agent()
    checker = create_fact_checker_agent()
    writer = create_report_writer_agent()

    return Swarm(
        nodes=[
            researcher,
            analyst,
            checker,
            writer
        ],
        entry_point=researcher,
        max_handoffs=8,
        max_iterations=10,
        execution_timeout=900,
        node_timeout=300,
        repetitive_handoff_detection_window=4,
        repetitive_handoff_min_unique_agents=2,
    )


def run_swarm(topic: str, conversation_history=None):

    conversation_history = conversation_history or []

    swarm = build_research_swarm()

    return swarm(
        f"""
Collaboratively research the user's current request and create
a complete cited research report.

PREVIOUS CONVERSATION:
{conversation_history}

CURRENT USER REQUEST:
{topic}

Use the previous conversation to understand follow-up questions.
Preserve the original topic when the user asks a follow-up.
If the user explicitly starts a new topic, focus on that topic.

RESEARCHER:
Gather evidence and source URLs.

ANALYST:
Analyze the actual research findings. Do not invent missing findings.

FACT CHECKER:
Review claims against the available evidence.

REPORT WRITER:
Produce the complete final Markdown report with references.

Pass relevant findings and results during handoffs.
Finish only when the report is complete.
"""
    )
