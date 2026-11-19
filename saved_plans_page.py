
import streamlit as st
from datetime import date, time

from plan_storage import (
    get_saved_plans,
    delete_saved_plan
)

from planner import verify_plan


def show_saved_plans_page():

    st.title("📁 Saved Study Plans")

    st.caption(
        "View and manage your approved study plans."
    )

    plans = get_saved_plans()

    total_minutes = sum(
        item["total_minutes"] for item in plans
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Approved Plans",
        len(plans)
    )

    col2.metric(
        "Total Planned Hours",
        round(total_minutes / 60, 1)
    )

    st.divider()

    if not plans:

        st.info(
            "No approved study plans yet. "
            "Generate and approve a plan first."
        )

        return

    for item in plans:

        plan_id = item["id"]

        with st.container(border=True):

            st.subheader(
                f"Study Plan — {item['study_date']}"
            )

            st.caption(
                f"Approved: {item['approved_at']}"
            )

            selected_date = date.fromisoformat(
                item["study_date"]
            )

            valid, problems = verify_plan(
                item["sessions"],
                selected_date,
                time.fromisoformat(
                    item["available_from"]
                ),
                time.fromisoformat(
                    item["available_until"]
                )
            )

            if valid:

                st.success(
                    "Approved — verification passed"
                )

            else:

                st.warning(
                    "This saved plan needs revision."
                )

                for problem in problems:
                    st.write(problem)

            if selected_date < date.today():

                st.caption("Past study plan")

            st.write(
                f"Total study time: "
                f"{item['total_minutes']} minutes"
            )

            with st.expander("View Study Sessions"):

                for session in item["sessions"]:

                    st.write(
                        f"**{session['start']} - "
                        f"{session['end']}**"
                    )

                    st.write(session["task"])

                    st.caption(
                        f"Priority: {session['priority']} | "
                        f"Deadline: {session['deadline']}"
                    )

                    st.divider()

            confirmed = st.checkbox(
                "Confirm deletion",
                key=f"confirm_plan_{plan_id}"
            )

            if st.button(
                "Delete Saved Plan",
                key=f"delete_plan_{plan_id}",
                disabled=not confirmed
            ):

                delete_saved_plan(plan_id)

                if (
                    st.session_state.get("saved_plan_id")
                    == plan_id
                ):

                    st.session_state.saved_plan_id = None
                    st.session_state.plan_status = "Pending"

                st.rerun()
