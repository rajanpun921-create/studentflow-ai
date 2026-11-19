
import streamlit as st
from datetime import date, time
import database as db

# 1. Application settings

st.set_page_config(
    page_title="AI Student Assistant",
    page_icon="📚",
    layout="wide"
)

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

st.sidebar.title("📚 Student Assistant")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "My Tasks", "Weekly Timetable"]
)

st.sidebar.divider()
st.sidebar.caption("AI Student Schedule and Task Assistant")
st.sidebar.caption("Development Version 3.0")
st.sidebar.success("Database connected")

# 4. Dashboard

if page == "Dashboard":

    st.title("🏠 Student Dashboard")

    st.write(
        "Welcome to your university planner!"
    )

    st.caption(
        date.today().strftime("%A, %d %B %Y")
    )

    tasks = db.get_tasks()
    classes = db.get_classes()

    total_tasks = len(tasks)
    completed_tasks = sum(task[4] for task in tasks)
    pending_tasks = total_tasks - completed_tasks

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Tasks", total_tasks)
    col2.metric("Completed", completed_tasks)
    col3.metric("Pending", pending_tasks)
    col4.metric("Classes", len(classes))

    st.divider()

    st.subheader("📅 Today's Classes")

    today = date.today().strftime("%A")

    today_classes = [
        item for item in classes if item[2] == today
    ]

    today_classes.sort(key=lambda item: item[3])

    if today_classes:

        for item in today_classes:

            with st.container(border=True):

                st.write(f"**{item[1]}**")

                st.caption(
                    f"{item[3][:5]} - {item[4][:5]}"
                    f" | Room: {item[5] or 'Not specified'}"
                )

    else:
        st.info("No classes scheduled for today.")

    st.divider()

    st.subheader("📋 Upcoming Tasks")

    pending = [
        task for task in tasks if not task[4]
    ]

    if pending:

        for task in pending[:5]:

            with st.container(border=True):

                st.write(f"**{task[1]}**")

                st.caption(
                    f"Due: {task[2]} | Priority: {task[3]}"
                )

                if task[2] < date.today().isoformat():
                    st.error("Overdue")

                elif task[2] == date.today().isoformat():
                    st.warning("Due today")

    else:
        st.success("No pending tasks!")

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

st.sidebar.divider()
st.sidebar.caption("Built for university students.")
