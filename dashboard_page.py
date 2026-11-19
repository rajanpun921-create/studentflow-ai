
import streamlit as st
from datetime import date
import database as db

from plan_storage import get_saved_plans
from styles import show_welcome_banner


def show_dashboard():

    today = date.today()
    current_day = today.strftime("%A")

    tasks = db.get_tasks()
    classes = db.get_classes()
    saved_plans = get_saved_plans()

    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks if task[4]
    )

    pending_tasks = total_tasks - completed_tasks

    progress = (
        completed_tasks / total_tasks
        if total_tasks > 0 else 0
    )

    # Dashboard header

    st.title("Student Dashboard")

    st.caption(
        today.strftime("%A, %d %B %Y")
    )

    show_welcome_banner()

    # Live statistics

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Tasks",
        total_tasks
    )

    col2.metric(
        "Completed",
        completed_tasks
    )

    col3.metric(
        "Pending",
        pending_tasks
    )

    col4.metric(
        "Weekly Classes",
        len(classes)
    )

    st.divider()

    # Study progress

    st.subheader("📊 Your Study Progress")

    st.progress(progress)

    st.caption(
        f"{completed_tasks} of {total_tasks} "
        f"assignments completed "
        f"({progress * 100:.0f}%)"
    )

    st.metric(
        "Approved Study Plans",
        len(saved_plans)
    )

    st.divider()

    # Classes and upcoming deadlines

    left, right = st.columns(2)

    with left:

        st.subheader("📅 Today's Classes")

        today_classes = [
            item for item in classes
            if item[2] == current_day
        ]

        today_classes.sort(
            key=lambda item: item[3]
        )

        if not today_classes:

            st.info("No classes scheduled today.")

        else:

            for item in today_classes:

                with st.container(border=True):

                    st.markdown(
                        f"**{item[1]}**"
                    )

                    st.write(
                        f"🕒 {item[3]} – {item[4]}"
                    )

                    st.caption(
                        f"📍 Room: {item[5]}"
                    )

    with right:

        st.subheader("📌 Upcoming Deadlines")

        upcoming_tasks = [
            task for task in tasks
            if not task[4]
        ]

        upcoming_tasks.sort(
            key=lambda task: task[2]
        )

        if not upcoming_tasks:

            st.success(
                "All tasks are completed!"
            )

        else:

            for task in upcoming_tasks[:5]:

                with st.container(border=True):

                    st.markdown(
                        f"**{task[1]}**"
                    )

                    st.caption(
                        f"Deadline: {task[2]}"
                    )

                    if task[2] < today.isoformat():

                        st.error(
                            f"Overdue | {task[3]} priority"
                        )

                    elif task[3] == "High":

                        st.error("High priority")

                    elif task[3] == "Medium":

                        st.warning("Medium priority")

                    else:

                        st.info(
                            f"{task[3]} priority"
                        )

    st.divider()

    # AI assistant information

    st.subheader("🤖 Your AI Study Assistant")

    st.info(
        "Need help organizing your assignments? "
        "Visit AI Study Assistant for personalized "
        "recommendations or Intelligent Planner "
        "to generate a verified study schedule."
    )

    st.caption(
        "StudentFlow AI • Powered by Gemini AI, "
        "Python, Streamlit and SQLite."
    )
