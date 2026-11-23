import streamlit as st

from frontend.services.api_client import (
    get_history,
    get_research,
    get_sessions,
    get_session,
    delete_research,
    delete_session,
)

from frontend.components.theme import (
    apply_theme,
    page_header,
    section_header,
)

from frontend.components.sidebar import render_sidebar
from frontend.components.report_viewer import render_report
from frontend.components.research_card import render_research_card


# ==================================================
# PAGE SETUP
# ==================================================

apply_theme()
render_sidebar()

page_header(
    "YOUR RESEARCH LIBRARY",
    "Research History",
    "Find previous investigations, revisit reports, and manage conversations.",
)


# ==================================================
# TABS
# ==================================================

reports_tab, conversations_tab = st.tabs(
    ["📄  Research Reports", "💬  Conversations"]
)


# ==================================================
# REPORT HISTORY
# ==================================================

with reports_tab:

    try:
        records = get_history(100)

        completed_count = sum(
            1 for r in records
            if str(r.get("status", "")).lower() == "completed"
        )

        failed_count = sum(
            1 for r in records
            if str(r.get("status", "")).lower() == "failed"
        )

        metric1, metric2, metric3 = st.columns(3)

        metric1.metric("Saved reports", len(records))
        metric2.metric("Completed", completed_count)
        metric3.metric("Failed", failed_count)

        section_header("Your research library")

        if not records:
            st.info(
                "Your research library is empty. Start a research task "
                "and your saved reports will appear here."
            )
            st.page_link(
                "pages/new_research.py",
                label="✦ Start your first research",
            )

        else:
            search_col, filter_col = st.columns([2, 1])

            with search_col:
                search = st.text_input(
                    "Search research",
                    placeholder="Search by topic...",
                    key="report_search",
                )

            modes = sorted({
                r.get("mode", "unknown")
                for r in records
            })

            with filter_col:
                selected_mode = st.selectbox(
                    "Orchestration mode",
                    ["All modes"] + modes,
                    key="report_mode_filter",
                )

            filtered = records

            if search.strip():
                query = search.strip().lower()
                filtered = [
                    r for r in filtered
                    if query in r.get("topic", "").lower()
                ]

            if selected_mode != "All modes":
                filtered = [
                    r for r in filtered
                    if r.get("mode") == selected_mode
                ]

            st.caption(
                f"{len(filtered)} matching reports · "
                f"Showing up to 100 saved records"
            )

            if not filtered:
                st.info("No reports match your search.")

            else:
                report_options = {
                    (
                        f"#{r['id']}  ·  "
                        f"{r.get('topic', 'Untitled')[:100]}"
                    ): r["id"]
                    for r in filtered
                }

                selected_label = st.selectbox(
                    "Select a report to view",
                    list(report_options.keys()),
                    key="selected_report_history",
                )

                research_id = report_options[selected_label]

                selected_record = next(
                    r for r in filtered
                    if r["id"] == research_id
                )

                render_research_card(selected_record)

                open_col, delete_col = st.columns(2)

                with open_col:
                    if st.button(
                        "Open full report",
                        type="primary",
                        use_container_width=True,
                        key=f"open_report_{research_id}",
                    ):
                        try:
                            st.session_state.opened_history_report = (
                                get_research(research_id)
                            )
                            st.session_state.confirm_delete_research = None
                        except Exception as exc:
                            st.error(f"Could not open report: {exc}")

                with delete_col:
                    if st.button(
                        "Delete report",
                        use_container_width=True,
                        key=f"delete_report_{research_id}",
                    ):
                        st.session_state.confirm_delete_research = research_id

                opened = st.session_state.get("opened_history_report")

                if opened and opened.get("id") == research_id:
                    render_report(
                        report=opened.get("report", ""),
                        title=opened.get("topic", "Research Report"),
                        key=f"history_{research_id}",
                    )

                if (
                    st.session_state.get("confirm_delete_research")
                    == research_id
                ):
                    st.warning(
                        "This will permanently delete the report and its "
                        "associated conversation messages."
                    )

                    confirm_col, cancel_col = st.columns(2)

                    with confirm_col:
                        if st.button(
                            "Confirm deletion",
                            type="primary",
                            use_container_width=True,
                            key=f"confirm_report_{research_id}",
                        ):
                            try:
                                delete_research(research_id)

                                opened = st.session_state.get(
                                    "opened_history_report"
                                )

                                if opened and opened.get("id") == research_id:
                                    st.session_state.pop(
                                        "opened_history_report",
                                        None,
                                    )

                                st.session_state.pop(
                                    "confirm_delete_research",
                                    None,
                                )

                                st.success("Report deleted successfully.")
                                st.rerun()

                            except Exception as exc:
                                st.error(f"Could not delete report: {exc}")

                    with cancel_col:
                        if st.button(
                            "Cancel",
                            use_container_width=True,
                            key=f"cancel_report_{research_id}",
                        ):
                            st.session_state.pop(
                                "confirm_delete_research",
                                None,
                            )
                            st.rerun()

    except Exception as exc:
        st.error(f"Could not load research reports: {exc}")


# ==================================================
# CONVERSATION HISTORY
# ==================================================

with conversations_tab:

    section_header("Saved conversations")

    try:
        sessions = get_sessions()

        if not sessions:
            st.info("No conversations have been saved yet.")

        else:
            session_options = {}

            for session in sessions:
                session_id = session["id"]
                last_message = session.get(
                    "last_message",
                    "New conversation",
                )
                message_count = session.get("messages", 0)

                session_options[
                    f"{session_id[:8]}  ·  {last_message[:75]}  ·  {message_count} messages"
                ] = session_id

            selected_label = st.selectbox(
                "Choose a conversation",
                list(session_options.keys()),
                key="history_session_select",
            )

            session_id = session_options[selected_label]

            open_col, delete_col = st.columns(2)

            with open_col:
                if st.button(
                    "Open conversation",
                    type="primary",
                    use_container_width=True,
                    key=f"open_session_{session_id}",
                ):
                    try:
                        st.session_state.opened_research_session = (
                            get_session(session_id)
                        )
                        st.session_state.opened_research_session_id = (
                            session_id
                        )
                        st.session_state.confirm_delete_session = None
                    except Exception as exc:
                        st.error(f"Could not open conversation: {exc}")

            with delete_col:
                if st.button(
                    "Delete conversation",
                    use_container_width=True,
                    key=f"delete_session_{session_id}",
                ):
                    st.session_state.confirm_delete_session = session_id

            if (
                st.session_state.get("confirm_delete_session")
                == session_id
            ):
                st.warning(
                    "This permanently deletes the conversation and its "
                    "messages. Reports referenced by other conversations "
                    "may remain saved."
                )

                confirm_col, cancel_col = st.columns(2)

                with confirm_col:
                    if st.button(
                        "Confirm deletion",
                        type="primary",
                        use_container_width=True,
                        key=f"confirm_session_{session_id}",
                    ):
                        try:
                            delete_session(session_id)

                            st.session_state.pop(
                                "confirm_delete_session",
                                None,
                            )

                            if (
                                st.session_state.get(
                                    "opened_research_session_id"
                                ) == session_id
                            ):
                                st.session_state.pop(
                                    "opened_research_session",
                                    None,
                                )
                                st.session_state.pop(
                                    "opened_research_session_id",
                                    None,
                                )

                            st.success("Conversation deleted.")
                            st.rerun()

                        except Exception as exc:
                            st.error(f"Could not delete conversation: {exc}")

                with cancel_col:
                    if st.button(
                        "Cancel",
                        use_container_width=True,
                        key=f"cancel_session_{session_id}",
                    ):
                        st.session_state.pop(
                            "confirm_delete_session",
                            None,
                        )
                        st.rerun()

            conversation = st.session_state.get(
                "opened_research_session"
            )

            opened_id = st.session_state.get(
                "opened_research_session_id"
            )

            if conversation and opened_id == session_id:
                st.divider()
                section_header("Conversation preview")

                for message in conversation.get("messages", []):
                    role = message.get("role", "assistant")

                    if role not in ("user", "assistant"):
                        role = "assistant"

                    with st.chat_message(role):
                        st.markdown(message.get("content", ""))

    except Exception as exc:
        st.error(f"Could not load conversations: {exc}")