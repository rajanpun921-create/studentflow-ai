
import calendar
from datetime import date, datetime
from html import escape
from zoneinfo import ZoneInfo

import streamlit as st
import database as db
from plan_storage import get_saved_plans


def korean_today():
    try:
        return datetime.now(ZoneInfo("Asia/Seoul")).date()
    except Exception:
        return date.today()


def safe(value):
    return escape(str(value), quote=True)


def month_offset(day, offset):
    year, month = divmod(
        day.year * 12 + day.month - 1 + offset, 12
    )
    return date(year, month + 1, 1)


def calendar_html(month, today, pending):

    counts = {}

    for task in pending:
        key = str(task[2])
        counts[key] = counts.get(key, 0) + 1

    cells = [
        f'<div class="sf-weekday">{name}</div>'
        for name in (
            "MON", "TUE", "WED", "THU",
            "FRI", "SAT", "SUN"
        )
    ]

    for week in calendar.Calendar(
        firstweekday=0
    ).monthdatescalendar(month.year, month.month):

        for day in week:

            count = counts.get(day.isoformat(), 0)
            classes = "sf-day"

            if day.month != month.month:
                classes += " sf-outside"
                count = 0

            if day == today:
                classes += " sf-today"

            dot = (
                '<span class="sf-dot"></span>'
                if count else ''
            )

            label = safe(
                f"{day:%d %b %Y} — "
                f"{count} pending deadline(s)"
            )

            cells.append(
                f'<div class="{classes}" '
                f'title="{label}" aria-label="{label}">'
                f'<span>{day.day}</span>{dot}</div>'
            )

    return (
        f'<div class="sf-calendar">'
        f'{"".join(cells)}</div>'
    )


def build_dashboard(
    tasks, classes, saved_plans, today, month
):

    total = len(tasks)
    completed = sum(bool(t[4]) for t in tasks)

    pending = sorted(
        (t for t in tasks if not t[4]),
        key=lambda t: (
            str(t[2]),
            {
                "High": 0,
                "Medium": 1,
                "Low": 2
            }.get(t[3], 3)
        )
    )

    percent = round(
        100 * completed / total
    ) if total else 0

    high = sum(
        t[3] == "High" for t in pending
    )

    overdue = sum(
        str(t[2]) < today.isoformat()
        for t in pending
    )

    today_classes = sorted(
        (
            c for c in classes
            if c[2] == today.strftime("%A")
        ),
        key=lambda c: c[3]
    )

    # Statistics cards

    metrics = ''.join(
        f'''
        <div class="sf-metric">
            <span class="sf-icon {color}">
                {icon}
            </span>
            <div>
                <div class="sf-muted">{label}</div>
                <strong>{value}</strong>
            </div>
        </div>
        '''
        for icon, color, label, value in [
            (
                "▤", "sf-blue",
                "Total tasks", total
            ),
            (
                "✓", "sf-green",
                "Completed", completed
            ),
            (
                "▦", "sf-violet",
                "Weekly classes", len(classes)
            ),
            (
                "◷", "sf-teal",
                "Approved plans", len(saved_plans)
            )
        ]
    )

    # Upcoming assignment deadlines

    task_rows = []

    for t in pending[:5]:

        due = str(t[2])

        try:
            pretty_due = date.fromisoformat(
                due
            ).strftime("%d %b %Y")
        except ValueError:
            pretty_due = due

        priority = safe(t[3])

        if due < today.isoformat():

            status = f"Overdue · {priority}"
            color = "red"

        elif due == today.isoformat():

            status = f"Today · {priority}"

            color = (
                "red"
                if t[3] == "High"
                else "amber"
            )

        else:

            status = f"{priority} priority"

            color = {
                "High": "red",
                "Medium": "amber",
                "Low": "green"
            }.get(t[3], "blue")

        task_rows.append(
            f'''
            <div class="sf-task">

                <div class="sf-task-main">

                    <span class="sf-task-icon">
                        ▤
                    </span>

                    <div>
                        <strong>{safe(t[1])}</strong>
                        <small>
                            Due {safe(pretty_due)}
                        </small>
                    </div>

                </div>

                <span class="sf-pill sf-{color}">
                    {status}
                </span>

            </div>
            '''
        )

    task_markup = ''.join(task_rows) or '''
        <div class="sf-empty">
            No pending tasks.
            Add an assignment in My Tasks.
        </div>
    '''

    # Today's university classes

    class_rows = ''.join(
        f'''
        <tr>
            <td><strong>{safe(c[1])}</strong></td>
            <td>
                {safe(str(c[3])[:5])}–
                {safe(str(c[4])[:5])}
            </td>
            <td>
                {safe(c[5] or "Not specified")}
            </td>
        </tr>
        '''
        for c in today_classes
    )

    if class_rows:

        class_markup = f'''
        <div class="sf-table-wrap">

            <table class="sf-table">

                <thead>
                    <tr>
                        <th>Subject</th>
                        <th>Time</th>
                        <th>Room</th>
                    </tr>
                </thead>

                <tbody>
                    {class_rows}
                </tbody>

            </table>

        </div>
        '''

    else:

        class_markup = '''
        <div class="sf-empty">
            No university classes scheduled today.
        </div>
        '''

    # Progress chart

    ring_background = (
        f'conic-gradient('
        f'#2563eb 0% {percent}%, '
        f'#dbe5f4 {percent}% 100%)'
    )

    plan_minutes = sum(
        int(p.get("total_minutes", 0))
        for p in saved_plans
    )

    hours, minutes = divmod(plan_minutes, 60)

    # Main dashboard layout

    return f'''

    <div class="sf-dashboard">

        <div class="sf-grid">

            <section class="sf-hero">

                <div>

                    <div class="sf-eyebrow">
                        YOUR STUDENT WORKSPACE
                    </div>

                    <h2>
                        Make today productive.
                        <span>✦</span>
                    </h2>

                    <p>
                        Organize your classes,
                        stay ahead of assignments
                        and plan smarter with AI.
                    </p>

                    <div class="sf-hero-note">
                        {len(pending)} pending tasks
                        · {overdue} overdue
                    </div>

                </div>

                <div class="sf-hero-right">

                    <strong>{percent}%</strong>

                    <span>Tasks completed</span>

                    <div class="sf-hero-track">
                        <i style="width:{percent}%">
                        </i>
                    </div>

                </div>

            </section>

            <section class="sf-card sf-metrics">
                {metrics}
            </section>

            <div class="sf-stack">

                <section class="sf-card">

                    <header class="sf-heading">

                        <h3>Upcoming deadlines</h3>

                        <span>
                            {high} high priority
                        </span>

                    </header>

                    {task_markup}

                    <div class="sf-note">
                        Manage assignments from
                        My Tasks in the sidebar.
                    </div>

                </section>

                <section class="sf-card">

                    <header class="sf-heading">

                        <h3>Today's classes</h3>

                        <span>
                            {len(today_classes)}
                            scheduled
                        </span>

                    </header>

                    {class_markup}

                </section>

                <section class="sf-assistant">

                    <span class="sf-assistant-icon">
                        ✦
                    </span>

                    <div>

                        <strong>
                            Your AI study assistant
                        </strong>

                        <p>
                            Use AI Study Assistant
                            for recommendations, or
                            Intelligent Planner to
                            create a verified
                            study schedule.
                        </p>

                    </div>

                </section>

            </div>

            <div class="sf-stack">

                <section class="sf-card">

                    <header class="sf-heading">

                        <h3>{month:%B %Y}</h3>

                        <span>Calendar</span>

                    </header>

                    {calendar_html(month, today, pending)}

                    <div class="sf-calendar-legend">

                        <span>
                            <i class="sf-legend-today"></i>
                            Today
                        </span>

                        <span>
                            <i class="sf-legend-due"></i>
                            Pending deadline
                        </span>

                    </div>

                </section>

                <section class="sf-card">

                    <header class="sf-heading">

                        <h3>Study progress</h3>

                        <span>All tasks</span>

                    </header>

                    <div class="sf-progress">

                        <div
                            class="sf-ring"
                            style="background:{ring_background}"
                            role="img"
                            aria-label="{percent}% tasks completed"
                        >

                            <div>
                                <strong>{percent}%</strong>
                                <small>Completed</small>
                            </div>

                        </div>

                        <div class="sf-progress-key">

                            <div>
                                <i style="background:#2563eb">
                                </i>
                                Completed
                                <b>{completed}</b>
                            </div>

                            <div>
                                <i style="background:#dbe5f4">
                                </i>
                                Pending
                                <b>{len(pending)}</b>
                            </div>

                            <p>
                                {hours}h {minutes}m
                                in saved study plans
                                <br>
                                <small>
                                    Planned time,
                                    not measured study time
                                </small>
                            </p>

                        </div>

                    </div>

                </section>

            </div>

        </div>

        <footer class="sf-footer">
            StudentFlow AI · Python · Streamlit
            · SQLite · Gemini AI
        </footer>

    </div>

    '''


def show_dashboard():

    today = korean_today()

    tasks = db.get_tasks()
    classes = db.get_classes()
    saved_plans = get_saved_plans()

    heading, control = st.columns([2, 1])

    with heading:

        st.title("Student Dashboard")

        st.caption(
            today.strftime("%A, %d %B %Y")
        )

    with control:

        months = [
            month_offset(today, i)
            for i in range(-12, 13)
        ]

        month = st.selectbox(
            "Calendar month",
            months,
            index=12,
            format_func=lambda d: d.strftime(
                "%B %Y"
            ),
            key="sf_dashboard_month"
        )

    html = build_dashboard(
        tasks,
        classes,
        saved_plans,
        today,
        month
    )

    st.markdown(
        ''.join(
            line.strip()
            for line in html.splitlines()
        ),
        unsafe_allow_html=True
    )
