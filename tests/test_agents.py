def test_agent_factories_are_importable():
    from agents.planner import create_planner_agent
    from agents.researcher import create_researcher_agent
    from agents.analyst import create_analyst_agent
    from agents.fact_checker import create_fact_checker_agent
    from agents.report_writer import create_report_writer_agent
    assert all(callable(fn) for fn in [
        create_planner_agent, create_researcher_agent, create_analyst_agent,
        create_fact_checker_agent, create_report_writer_agent
    ])
