import streamlit as st


def render_research_card(item):

    topic = item.get("topic", "Untitled research")
    research_id = item.get("id", "N/A")
    mode = item.get("mode", "unknown")
    status = str(item.get("status", "unknown")).lower()
    created_at = item.get("created_at", "")

    status_details = {
        "completed": ("🟢", "Completed"),
        "failed": ("🔴", "Failed"),
        "processing": ("🟡", "Processing"),
        "running": ("🟡", "Running"),
        "pending": ("⚪", "Pending"),
    }

    icon, status_label = status_details.get(
        status,
        ("⚪", status.title()),
    )

    with st.container(border=True):

        st.markdown(f"### {topic}")

        id_col, mode_col, status_col = st.columns(3)

        with id_col:
            st.caption("REPORT ID")
            st.markdown(f"**#{research_id}**")

        with mode_col:
            st.caption("ORCHESTRATION")
            st.markdown(f"**{mode.replace('_', ' ').title()}**")

        with status_col:
            st.caption("STATUS")
            st.markdown(f"**{icon} {status_label}**")

        if created_at:
            st.caption(f"Created: {created_at}")