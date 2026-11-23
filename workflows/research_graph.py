
from strands.multiagent import GraphBuilder

from agents.planner import create_planner_agent
from agents.researcher import create_researcher_agent
from agents.analyst import create_analyst_agent
from agents.fact_checker import create_fact_checker_agent
from agents.report_writer import create_report_writer_agent


def build_research_graph():

    builder = GraphBuilder()

    planner = builder.add_node(
        create_planner_agent(),
        node_id="planner"
    )

    researcher = builder.add_node(
        create_researcher_agent(),
        node_id="researcher"
    )

    analyst = builder.add_node(
        create_analyst_agent(),
        node_id="analyst"
    )

    checker = builder.add_node(
        create_fact_checker_agent(),
        node_id="fact_checker"
    )

    writer = builder.add_node(
        create_report_writer_agent(),
        node_id="report_writer"
    )

    builder.add_edge(planner, researcher)
    builder.add_edge(researcher, analyst)
    builder.add_edge(analyst, checker)
    builder.add_edge(checker, writer)

    builder.set_entry_point("planner")
    builder.set_max_node_executions(5)
    builder.set_execution_timeout(900)
    builder.set_node_timeout(300)

    return builder.build()


def run_graph(topic: str, conversation_history=None):

    conversation_history = conversation_history or []

    graph = build_research_graph()

    return graph(
        f"""
Research the user's current request and produce a referenced report.

PREVIOUS CONVERSATION:
{conversation_history}

CURRENT USER REQUEST:
{topic}

Use the previous conversation to understand follow-up questions.
If the user explicitly starts a new topic, focus on that topic.
Pass relevant research findings through the graph.
Produce a complete final report with source references.
"""
    )
