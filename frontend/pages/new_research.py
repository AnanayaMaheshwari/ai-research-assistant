import streamlit as st

from frontend.services.api_client import (
    create_session,
    get_session,
    stream_research,
)

from frontend.components.theme import (
    apply_theme,
    page_header,
    hero_card,
    section_header,
)

from frontend.components.sidebar import render_sidebar


# ==================================================
# PAGE SETUP
# ==================================================

apply_theme()
render_sidebar()

page_header(
    "AI RESEARCH WORKSPACE",
    "New Research",
    "Start an investigation and collaborate with your AI research team.",
)

hero_card(
    "✦ YOUR AI RESEARCH TEAM",
    "What would you like to discover today?",
    "Describe a topic, question, or problem. Your research agents will "
    "plan the investigation, gather information, analyse findings, "
    "verify claims, and prepare a structured report.",
)


# ==================================================
# SESSION MANAGEMENT
# ==================================================

if "research_session_id" not in st.session_state:
    try:
        session = create_session()
        st.session_state.research_session_id = session["session_id"]
    except Exception as exc:
        st.error(f"Could not create research session: {exc}")
        st.stop()

session_id = st.session_state.research_session_id


# ==================================================
# SESSION BAR
# ==================================================

session_col, new_col = st.columns([3, 1])

with session_col:
    st.caption(f"ACTIVE CONVERSATION  ·  `{session_id[:8]}`")

with new_col:
    if st.button("＋ New conversation", use_container_width=True):
        try:
            session = create_session()
            st.session_state.research_session_id = session["session_id"]
            st.rerun()
        except Exception as exc:
            st.error(f"Could not create a conversation: {exc}")


# ==================================================
# CONVERSATION
# ==================================================

try:
    conversation = get_session(session_id)
    messages = conversation.get("messages", [])

    if messages:
        section_header("Conversation")

        for message in messages:
            role = message.get("role", "assistant")
            if role not in ("user", "assistant"):
                role = "assistant"

            with st.chat_message(role):
                st.markdown(message.get("content", ""))

except Exception as exc:
    st.warning(f"Could not load conversation history: {exc}")


# ==================================================
# RESEARCH INPUT
# ==================================================

section_header("Create a research task")

mode_options = {
    "Sequential": {
        "value": "sequential",
        "description": "Agents complete each research stage in order.",
        "icon": "🔗",
    },
    "Agents as Tools": {
        "value": "agents_as_tools",
        "description": "A lead agent delegates tasks to specialist agents.",
        "icon": "🧠",
    },
    "Graph": {
        "value": "graph",
        "description": "A structured graph controls the workflow.",
        "icon": "🕸️",
    },
    "Swarm": {
        "value": "swarm",
        "description": "Agents collaborate through a swarm workflow.",
        "icon": "🐝",
    },
}

with st.form("research_form", clear_on_submit=True):

    topic = st.text_area(
        "Research question or topic",
        height=150,
        placeholder=(
            "Example: Analyse the impact of generative AI on healthcare. "
            "Explore current applications, recent developments, risks, "
            "and future opportunities."
        ),
        label_visibility="collapsed",
    )

    st.markdown("**Choose an orchestration pattern**")

    selected_mode = st.selectbox(
        "Orchestration pattern",
        list(mode_options.keys()),
        index=0,
        label_visibility="collapsed",
    )

    st.caption(mode_options[selected_mode]["description"])

    submitted = st.form_submit_button(
        "✦ Start Research",
        type="primary",
        use_container_width=True,
    )


# ==================================================
# RUN RESEARCH
# ==================================================

if submitted:

    if not topic.strip():
        st.warning("Enter a research topic before starting.")

    else:
        research_topic = topic.strip()
        mode = mode_options[selected_mode]["value"]

        with st.chat_message("user"):
            st.markdown(research_topic)

        with st.chat_message("assistant"):

            status = st.status(
                "Preparing your AI research team...",
                expanded=True,
            )

            report_placeholder = st.empty()
            streamed_report = ""
            completed = False

            try:
                for event in stream_research(
                    research_topic,
                    mode,
                    session_id,
                ):

                    event_type = event.get("type")

                    if event_type == "stage":
                        status.write(
                            f"⚙️ {event.get('message', 'Research in progress...')}"
                        )

                    elif event_type == "token":
                        streamed_report += event.get("text", "")
                        report_placeholder.markdown(
                            streamed_report + "▍"
                        )

                    elif event_type == "complete":
                        result = event.get("result", {})
                        final_report = result.get(
                            "report",
                            streamed_report,
                        )

                        if final_report:
                            report_placeholder.markdown(final_report)

                        report_id = result.get("id")
                        completion_message = "Research completed successfully."

                        if report_id is not None:
                            completion_message += f" Report #{report_id} saved."

                        status.update(
                            label=completion_message,
                            state="complete",
                            expanded=False,
                        )

                        completed = True

                    elif event_type == "error":
                        raise RuntimeError(
                            event.get(
                                "message",
                                "Unknown research error",
                            )
                        )

                if completed:
                    st.rerun()
                else:
                    status.update(
                        label="Research ended without a completion event.",
                        state="error",
                    )

                    if streamed_report:
                        st.warning("A partial report was received.")

            except Exception as exc:
                status.update(
                    label="Research failed",
                    state="error",
                )
                st.error(f"Research request failed: {exc}")