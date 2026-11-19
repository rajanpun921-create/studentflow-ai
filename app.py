
import streamlit as st
from datetime import date, time
import database as db
from ai_page import show_ai_page
from planner_page import show_planner_page
from saved_plans_page import show_saved_plans_page
from styles import (
    apply_styles,
    show_welcome_banner
)
from dashboard_page import show_dashboard

# 1. Application settings


st.set_page_config(
    page_title="StudentFlow AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="auto"
)

apply_styles()

# 2. Initialize SQLite database

db.initialize_database()

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

# 3. Sidebar navigation


st.sidebar.title("🎓 StudentFlow AI")

st.sidebar.caption(
    "Plan smarter. Study better."
)



page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "My Tasks",
        "Weekly Timetable",
        "AI Study Assistant",
        "Intelligent Planner",
        "Saved Study Plans"
    ]
)


st.sidebar.divider()
st.sidebar.caption("AI Student Schedule and Task Assistant")
st.sidebar.caption("Version 6.0")
st.sidebar.success("Database connected")

# 4. Dashboard

if page == "Dashboard":

    show_dashboard()
# 5. Task Manager

elif page == "My Tasks":

    st.title("📝 My Tasks")

    with st.form("task_form", clear_on_submit=True):

        task_name = st.text_input("Task Name")

        due_date = st.date_input(
            "Due Date",
            value=date.today()
        )

        priority = st.selectbox(
            "Priority",
            ["High", "Medium", "Low"]
        )

        submitted = st.form_submit_button("Add Task")

        if submitted:

            if task_name.strip():

                db.add_task(
                    task_name.strip(),
                    due_date,
                    priority
                )

                st.success("Task saved successfully!")

            else:
                st.warning("Please enter a task name.")

    st.divider()

    st.subheader("Your Tasks")

    tasks = db.get_tasks()

    if not tasks:
        st.info("No tasks found.")

    for task in tasks:

        task_id, name, due, priority, done = task

        with st.container(border=True):

            st.write(f"**{name}**")

            st.caption(
                f"Due: {due} | Priority: {priority}"
            )

            completed = st.checkbox(
                "Completed",
                value=bool(done),
                key=f"task_{task_id}"
            )

            if completed != bool(done):

                db.update_task_status(
                    task_id,
                    completed
                )

                st.rerun()

            if st.button(
                "Delete Task",
                key=f"delete_task_{task_id}"
            ):

                db.delete_task(task_id)
                st.rerun()

# 6. Weekly Timetable

elif page == "Weekly Timetable":

    st.title("📅 Weekly University Timetable")

    with st.form("class_form", clear_on_submit=True):

        subject = st.text_input("Subject Name")

        day = st.selectbox("Day", days)

        col1, col2 = st.columns(2)

        with col1:

            start_time = st.time_input(
                "Start Time",
                value=time(9, 0)
            )

        with col2:

            end_time = st.time_input(
                "End Time",
                value=time(10, 30)
            )

        room = st.text_input("Classroom")

        submitted = st.form_submit_button("Add Class")

        if submitted:

            if not subject.strip():

                st.warning("Enter a subject name.")

            elif end_time <= start_time:

                st.error(
                    "End time must be later than start time."
                )

            else:

                db.add_class(
                    subject.strip(),
                    day,
                    start_time,
                    end_time,
                    room.strip()
                )

                st.success("Class saved successfully!")

    st.divider()

    st.subheader("Your Weekly Schedule")

    classes = db.get_classes()

    for selected_day in days:

        day_classes = [
            item for item in classes
            if item[2] == selected_day
        ]

        day_classes.sort(key=lambda item: item[3])

        with st.expander(
            selected_day,
            expanded=(
                selected_day == date.today().strftime("%A")
            )
        ):

            if not day_classes:

                st.caption("No classes scheduled.")

            for item in day_classes:

                class_id, subject, day, start, end, room = item

                st.write(f"**{subject}**")

                st.caption(
                    f"{start[:5]} - {end[:5]}"
                    f" | Room: {room or 'Not specified'}"
                )

                if st.button(
                    "Delete Class",
                    key=f"delete_class_{class_id}"
                ):

                    db.delete_class(class_id)
                    st.rerun()

# 7. Footer

elif page == "AI Study Assistant":

    show_ai_page()
elif page == "Intelligent Planner":

    show_planner_page()
elif page == "Saved Study Plans":

    show_saved_plans_page()
    st.sidebar.divider()
st.sidebar.caption("Built for university students.")
