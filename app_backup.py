
import streamlit as st
from datetime import date

# Application settings
st.set_page_config(
    page_title="AI Student Assistant",
    page_icon="📚",
    layout="wide"
)

# Temporary task storage
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "next_id" not in st.session_state:
    st.session_state.next_id = 1

# Application heading
st.title("📚 AI Student Schedule and Task Assistant")
st.write("Organize your university life in one place.")

st.divider()

# Dashboard
total_tasks = len(st.session_state.tasks)
completed_tasks = sum(
    1 for task in st.session_state.tasks if task["done"]
)
pending_tasks = total_tasks - completed_tasks

col1, col2, col3 = st.columns(3)

col1.metric("Total Tasks", total_tasks)
col2.metric("Completed", completed_tasks)
col3.metric("Pending", pending_tasks)

st.divider()

# Add a new task
st.header("➕ Add a New Task")

with st.form("task_form"):
    task_name = st.text_input(
        "Task Name",
        placeholder="Example: Complete Python assignment"
    )

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
            st.session_state.tasks.append({
                "id": st.session_state.next_id,
                "name": task_name.strip(),
                "due_date": due_date,
                "priority": priority,
                "done": False
            })

            st.session_state.next_id += 1
            st.success("Task added successfully!")
        else:
            st.warning("Please enter a task name.")

st.divider()

# Display tasks
st.header("📋 My Tasks")

if not st.session_state.tasks:
    st.info("You have no tasks yet. Add your first task above.")

else:
    for task in st.session_state.tasks:

        with st.container(border=True):
            col1, col2 = st.columns([4, 1])

            with col1:
                st.write("**" + task["name"] + "**")
                st.caption(
                    f"Due: {task['due_date']} | "
                    f"Priority: {task['priority']}"
                )

                task["done"] = st.checkbox(
                    "Completed",
                    value=task["done"],
                    key=f"done_{task['id']}"
                )

            with col2:
                st.write("")

                if st.button(
                    "Delete",
                    key=f"delete_{task['id']}"
                ):
                    st.session_state.tasks = [
                        item for item in st.session_state.tasks
                        if item["id"] != task["id"]
                    ]
                    st.rerun()

st.divider()

st.caption("First development version | AI features will be added later.")
