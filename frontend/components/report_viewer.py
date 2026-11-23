import streamlit as st


def render_report(
    report: str,
    title: str = "Research Report",
    key: str = "report",
):
    st.markdown("---")

    title_col, download_col = st.columns([3, 1])

    with title_col:
        st.markdown("### 📄 Research Report")
        st.caption(title)

    filename = "".join(
        c if c.isalnum() or c in ("-", "_") else "_"
        for c in title
    ).strip("_")

    if not filename:
        filename = "research_report"

    with download_col:
        st.download_button(
            "⬇ Download",
            data=report or "",
            file_name=f"{filename}.md",
            mime="text/markdown",
            key=f"download_{key}",
            use_container_width=True,
            disabled=not bool(report),
        )

    if report:
        with st.container(border=True):
            st.markdown(report)
    else:
        st.info("This report does not contain any content.")