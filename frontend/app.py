
import streamlit as st
from collections import Counter
from datetime import datetime

from frontend.services.api_client import health_check, get_history
from frontend.components.sidebar import render_sidebar


st.set_page_config(
    page_title="Research AI",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# DASHBOARD THEME
# ==================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #0b1020;
        color: #e5e7eb;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background: #10172a;
        border-right: 1px solid #25314b;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    h1, h2, h3, h4 {
        color: #f8fafc !important;
        letter-spacing: -0.4px;
    }

    p, label {
        color: #cbd5e1;
    }

    .page-eyebrow {
        color: #a5b4fc;
        font-size: 11px;
        font-weight: 750;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .hero-card {
        background:
            radial-gradient(
                circle at 90% 10%,
                rgba(129, 140, 248, 0.22),
                transparent 35%
            ),
            linear-gradient(120deg, #172544, #252052, #211a3e);
        border: 1px solid #3b3b70;
        border-radius: 20px;
        padding: 38px 40px;
        margin: 8px 0 28px 0;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.18);
    }

    .hero-tag {
        display: inline-block;
        background: rgba(129, 140, 248, 0.17);
        color: #c7d2fe;
        border: 1px solid rgba(165, 180, 252, 0.25);
        border-radius: 30px;
        padding: 7px 13px;
        font-size: 10px;
        font-weight: 750;
        letter-spacing: 1px;
        margin-bottom: 20px;
    }

    .hero-title {
        color: #ffffff;
        font-size: clamp(30px, 4vw, 43px);
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -1.2px;
        margin-bottom: 15px;
    }

    .hero-description {
        color: #cbd5e1;
        font-size: 14px;
        line-height: 1.8;
        max-width: 720px;
    }

    .section-heading {
        color: #f1f5f9;
        font-size: 19px;
        font-weight: 750;
        margin: 30px 0 15px 0;
        letter-spacing: -0.3px;
    }

    .section-subtitle {
        color: #94a3b8;
        font-size: 12px;
        margin-top: -10px;
        margin-bottom: 17px;
    }

    .panel-card {
        background: linear-gradient(145deg, #141e34, #111a2d);
        border: 1px solid #293650;
        border-radius: 15px;
        padding: 20px;
        min-height: 100%;
    }

    .panel-label {
        color: #a5b4fc;
        font-size: 11px;
        font-weight: 750;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .feature-card {
        background: linear-gradient(145deg, #17223a, #121b30);
        border: 1px solid #2b3955;
        border-radius: 16px;
        padding: 22px;
        min-height: 165px;
        transition: border-color 0.2s ease;
    }

    .feature-icon {
        font-size: 27px;
        margin-bottom: 14px;
    }

    .feature-title {
        color: #f1f5f9;
        font-size: 15px;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .feature-description {
        color: #94a3b8;
        font-size: 12px;
        line-height: 1.7;
    }

    .activity-card {
        background: #141e32;
        border: 1px solid #293650;
        border-radius: 13px;
        padding: 16px 18px;
        margin-bottom: 10px;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #17223a, #121b30);
        border: 1px solid #2b3955;
        border-radius: 14px;
        padding: 18px 20px;
        min-height: 115px;
    }

    [data-testid="stMetricLabel"] {
        color: #9caec7 !important;
        font-size: 12px;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-size: 28px;
        font-weight: 750;
    }

    [data-testid="stMetricDelta"] {
        font-size: 11px;
    }

    [data-testid="stProgressBar"] > div {
        background: #26334e;
        border-radius: 20px;
    }

    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #6366f1, #a78bfa);
        border-radius: 20px;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #121b30;
        border-color: #293650;
        border-radius: 14px;
    }

    .stButton > button,
    .stLinkButton > a {
        border-radius: 9px;
        font-weight: 650;
        border: 1px solid #3b4770;
        transition: all 0.2s ease;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(110deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
    }

    .stButton > button:hover,
    .stLinkButton > a:hover {
        border-color: #818cf8;
        color: #c7d2fe;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    [data-testid="stSelectbox"] > div > div {
        background: #121b30;
    }

    hr {
        border-color: #293650;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

render_sidebar()


# ==================================================
# HERO SECTION
# ==================================================

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-tag">✦ AI-POWERED RESEARCH WORKSPACE</div>
        <div class="hero-title">
            Turn complex questions<br>
            into meaningful insights.
        </div>
        <div class="hero-description">
            Research smarter with a coordinated team of AI agents.
            Explore topics, analyze evidence, verify findings and
            generate structured research reports in one workspace.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# BACKEND CONNECTION
# ==================================================

backend_connected = False

try:
    health = health_check()
    backend_connected = bool(health)

except Exception:
    health = {}


# ==================================================
# LOAD DASHBOARD DATA
# ==================================================

@st.cache_data(ttl=30)
def load_dashboard_data():
    return get_history(limit=100)


# ==================================================
# WORKSPACE HEADER
# ==================================================

st.markdown(
    '<div class="page-eyebrow">YOUR WORKSPACE</div>',
    unsafe_allow_html=True
)

header_col, refresh_col = st.columns([4, 1])

with header_col:
    st.markdown("## Welcome to Research AI")
    st.caption(
        "Your research activity, analytics and saved reports — all in one place."
    )

with refresh_col:
    st.write("")
    if st.button(
        "↻ Refresh Dashboard",
        use_container_width=True
    ):
        st.cache_data.clear()
        st.rerun()


if backend_connected:
    st.success(
        f"Backend connected · {health.get('status', 'Online')}"
    )
else:
    st.error(
        "Backend is offline. Start it using: "
        "`python -m uvicorn backend.main:app --reload`"
    )


# ==================================================
# DASHBOARD DATA
# ==================================================

try:
    records = load_dashboard_data()

    if not isinstance(records, list):
        records = []

    total_research = len(records)

    completed = sum(
        1 for record in records
        if str(record.get("status", "")).lower() == "completed"
    )

    pending = sum(
        1 for record in records
        if str(record.get("status", "")).lower()
        in ["pending", "processing", "running"]
    )

    failed = sum(
        1 for record in records
        if str(record.get("status", "")).lower() == "failed"
    )

    mode_counts = Counter(
        record.get("mode", "unknown").replace("_", " ").title()
        for record in records
    )


    # ==================================================
    # RESEARCH OVERVIEW
    # ==================================================

    st.markdown(
        '<div class="section-heading">Research Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">A snapshot of your latest research activity</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Research",
        total_research,
        help="Number of records among the latest 100 research projects."
    )

    c2.metric(
        "Completed",
        completed
    )

    c3.metric(
        "In Progress",
        pending
    )

    c4.metric(
        "Failed",
        failed
    )

    st.caption(
        "Statistics are calculated from the latest 100 research records."
    )


    # ==================================================
    # RESEARCH ANALYTICS
    # ==================================================

    st.markdown(
        '<div class="section-heading">Research Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Understand how your research workflows are being used</div>',
        unsafe_allow_html=True
    )

    chart_col, info_col = st.columns([1.5, 1])

    with chart_col:
        with st.container(border=True):
            st.markdown("#### Orchestration Modes")

            if mode_counts:
                st.bar_chart(
                    dict(mode_counts),
                    color="#818cf8"
                )
            else:
                st.info("No research data available yet.")

    with info_col:
        with st.container(border=True):
            st.markdown("#### Research Summary")

            if total_research > 0:
                completion_rate = (
                    completed / total_research
                ) * 100

                st.metric(
                    "Completion Rate",
                    f"{completion_rate:.1f}%"
                )

                st.progress(
                    completion_rate / 100
                )

                st.caption(
                    f"{completed} of {total_research} projects completed."
                )

            else:
                st.info(
                    "Start your first research project to see analytics."
                )

            st.divider()

            st.markdown("#### Available Modes")

            for mode, count in mode_counts.items():
                st.write(f"**{mode}:** {count}")


    # ==================================================
    # RECENT RESEARCH ACTIVITY
    # ==================================================

    st.markdown(
        '<div class="section-heading">Recent Research Activity</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Quick access to your latest saved research reports</div>',
        unsafe_allow_html=True
    )

    if records:

        for record in records[:8]:

            topic = record.get("topic", "Untitled Research")
            research_id = record.get("id")
            mode = record.get("mode", "sequential")
            status = record.get("status", "unknown")

            created_at = record.get("created_at", "")

            try:
                date = datetime.fromisoformat(
                    created_at.replace("Z", "+00:00")
                ).strftime("%d %b %Y · %I:%M %p")
            except (ValueError, TypeError, AttributeError):
                date = "Date unavailable"

            status_color = {
                "completed": "🟢",
                "failed": "🔴",
                "processing": "🟡",
                "running": "🟡",
                "pending": "⚪"
            }.get(str(status).lower(), "⚪")

            with st.container(border=True):

                left, right = st.columns([4, 1])

                with left:
                    st.markdown(f"**{topic}**")

                    st.caption(
                        f"ID: {research_id} · "
                        f"Mode: {mode.replace('_', ' ').title()} · "
                        f"{date}"
                    )

                with right:
                    st.write(
                        f"{status_color} {status.title()}"
                    )

                    if research_id is not None:
                        if st.button(
                            "View Report",
                            key=f"view_{research_id}",
                            use_container_width=True
                        ):
                            st.session_state["selected_research_id"] = research_id
                            st.switch_page(
                                "pages/research_history.py"
                            )

    else:
        with st.container(border=True):
            st.markdown("#### Your research journey starts here")
            st.write(
                "No research projects found. Start your first research project!"
            )

            st.page_link(
                "pages/new_research.py",
                label="✨ Start New Research"
            )


except Exception as exc:

    st.error(
        f"Unable to load dashboard research data: {exc}"
    )

    st.info(
        "Check that the backend is running and the database is accessible."
    )


# ==================================================
# QUICK ACTIONS
# ==================================================

st.markdown(
    '<div class="section-heading">Quick Actions</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">Jump directly to the tools you use most</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🔬</div>
            <div class="feature-title">Start New Research</div>
            <div class="feature-description">
                Explore a new topic using your AI research team.
                Plan, investigate and generate a structured report.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.page_link(
        "pages/new_research.py",
        label="Start researching →"
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <div class="feature-title">Research History</div>
            <div class="feature-description">
                Browse previous research reports, revisit conversations
                and manage your saved work.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.page_link(
        "pages/research_history.py",
        label="View history →"
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">⚙️</div>
            <div class="feature-title">Settings</div>
            <div class="feature-description">
                Review your model configuration and research
                workspace settings.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.page_link(
        "pages/settings.py",
        label="Open settings →"
    )


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

footer_col1, footer_col2 = st.columns([3, 1])

with footer_col1:
    st.caption(
        "Research AI · Powered by Strands Agents, Gemini and FastAPI"
    )

with footer_col2:
    st.caption("AI Research Workspace")
