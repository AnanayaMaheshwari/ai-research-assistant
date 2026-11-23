import streamlit as st

from backend.core.config import settings

from frontend.components.theme import (
    apply_theme,
    page_header,
    section_header,
)

from frontend.components.sidebar import render_sidebar


# ==================================================
# PAGE SETUP
# ==================================================

apply_theme()
render_sidebar()

page_header(
    "WORKSPACE CONFIGURATION",
    "Settings",
    "View your AI model, backend connection, and research workflow configuration.",
)


# ==================================================
# MODEL CONFIGURATION
# ==================================================

section_header("AI model configuration")

model_col, provider_col = st.columns(2)

with model_col:
    with st.container(border=True):
        st.caption("ACTIVE MODEL")
        st.markdown("### 🤖 Gemini")
        st.markdown(f"**{settings.gemini_model}**")
        st.caption("Configured through environment variables.")

with provider_col:
    with st.container(border=True):
        st.caption("MODEL PROVIDER")
        st.markdown("### Google")
        st.markdown("**Google Gemini API**")
        st.caption("Used by your Strands research agents.")


# ==================================================
# BACKEND CONFIGURATION
# ==================================================

section_header("Backend configuration")

with st.container(border=True):
    st.caption("BACKEND API URL")
    st.markdown(f"**{settings.backend_url}**")
    st.caption("Your frontend communicates with the backend through this URL.")


# ==================================================
# ORCHESTRATION MODES
# ==================================================

section_header("Research orchestration")

modes = [
    {
        "name": "Sequential",
        "code": "sequential",
        "icon": "🔗",
        "description": "Runs the research agents one after another in a defined sequence.",
    },
    {
        "name": "Agents as Tools",
        "code": "agents_as_tools",
        "icon": "🧠",
        "description": "A coordinating agent delegates tasks to specialist agents.",
    },
    {
        "name": "Graph",
        "code": "graph",
        "icon": "🕸️",
        "description": "Organises the research workflow as connected execution stages.",
    },
    {
        "name": "Swarm",
        "code": "swarm",
        "icon": "🐝",
        "description": "Allows agents to collaborate through a swarm workflow.",
    },
]

for start in range(0, len(modes), 2):
    columns = st.columns(2)

    for column, mode in zip(columns, modes[start:start + 2]):
        with column:
            with st.container(border=True):
                st.markdown(f"### {mode['icon']} {mode['name']}")
                st.caption(mode["description"])
                st.code(mode["code"])


# ==================================================
# AGENT PIPELINE
# ==================================================

section_header("AI agent pipeline")

agents = [
    ("01", "Planner", "Breaks the research topic into manageable tasks."),
    ("02", "Researcher", "Gathers relevant information and supporting findings."),
    ("03", "Analyst", "Analyses evidence and identifies important insights."),
    ("04", "Fact Checker", "Reviews claims and checks factual consistency."),
    ("05", "Report Writer", "Produces the final structured research report."),
]

for number, name, description in agents:
    with st.container(border=True):
        number_col, detail_col = st.columns([1, 5])

        with number_col:
            st.markdown(f"### `{number}`")

        with detail_col:
            st.markdown(f"**{name}**")
            st.caption(description)


# ==================================================
# SECURITY
# ==================================================

section_header("Security and environment")

with st.container(border=True):
    st.markdown("### 🔐 API credentials")
    st.success("API keys are not displayed in the application.")
    st.caption(
        "Credentials are loaded from the root `.env` file. "
        "Never commit this file to your Git repository."
    )

with st.container(border=True):
    st.markdown("### ⚙️ Configuration management")
    st.caption(
        "These settings are currently read-only. To change the model "
        "or backend URL, update the corresponding values in your `.env` "
        "file and restart the application."
    )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "Research AI · Strands Agents · Gemini · FastAPI · Streamlit"
)