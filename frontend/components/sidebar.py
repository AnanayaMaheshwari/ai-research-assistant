
import streamlit as st


def render_sidebar():

    # Hide Streamlit's automatically generated page navigation
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:

        st.markdown(
            """
            <div style="padding: 12px 4px 22px 4px;">
                <div style="
                    display:flex;
                    align-items:center;
                    gap:12px;
                    margin-bottom:8px;
                ">
                    <div style="
                        background:linear-gradient(135deg,#6366f1,#9333ea);
                        width:42px;
                        height:42px;
                        border-radius:12px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-size:22px;
                    ">🔎</div>
                    <div>
                        <div style="
                            color:#f8fafc;
                            font-size:19px;
                            font-weight:750;
                        ">Research AI</div>
                        <div style="
                            color:#94a3b8;
                            font-size:11px;
                        ">Intelligent research workspace</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("##### WORKSPACE")

        st.page_link(
            "app.py",
            label="Dashboard",
            icon=":material/dashboard:",
        )

        st.page_link(
            "pages/new_research.py",
            label="New Research",
            icon=":material/auto_awesome:",
        )

        st.page_link(
            "pages/research_history.py",
            label="Research History",
            icon=":material/history:",
        )

        st.page_link(
            "pages/settings.py",
            label="Settings",
            icon=":material/settings:",
        )

        st.divider()

        st.markdown("##### RESEARCH PIPELINE")

        pipeline = [
            ("01", "Planner"),
            ("02", "Researcher"),
            ("03", "Analyst"),
            ("04", "Fact Checker"),
            ("05", "Report Writer"),
        ]

        for number, name in pipeline:
            st.markdown(
                f"""
                <div style="
                    display:flex;
                    align-items:center;
                    gap:12px;
                    padding:7px 2px;
                ">
                    <span style="
                        color:#818cf8;
                        font-size:11px;
                        font-weight:700;
                    ">{number}</span>
                    <span style="
                        color:#cbd5e1;
                        font-size:13px;
                    ">{name}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.divider()

        st.caption("Powered by Strands Agents + Gemini")
        st.caption("FastAPI · Streamlit · MySQL")
