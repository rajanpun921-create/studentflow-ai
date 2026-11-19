
import database as db


# Convert clock time into minutes
def to_minutes(value):

    parts = str(value).split(":")

    return int(parts[0]) * 60 + int(parts[1])


# Convert minutes back into clock time
def to_clock(minutes):

    hours = minutes // 60
    remaining = minutes % 60

    return f"{hours:02d}:{remaining:02d}"


# Retrieve classes for a selected date
def get_daily_classes(selected_date):

    day = selected_date.strftime("%A")

    classes = db.get_classes()

    daily_classes = [
        item for item in classes
        if item[2] == day
    ]

    return sorted(
        daily_classes,
        key=lambda item: item[3]
    )


# Find available study periods
def get_free_slots(selected_date, start, end):

    start = to_minutes(start)
    end = to_minutes(end)

    if end <= start:

        raise ValueError(
            "End time must be after start time."
        )

    classes = get_daily_classes(selected_date)

    free_slots = []

    current = start

    for item in classes:

        class_start = to_minutes(item[3])
        class_end = to_minutes(item[4])

        if class_end <= current:
            continue

        if class_start >= end:
            break

        if class_start > current:

            free_slots.append(
                (current, class_start)
            )

        current = max(current, class_end)

    if current < end:

        free_slots.append((current, end))

    return free_slots


# Prioritize unfinished assignments
def get_prioritized_tasks():

    tasks = db.get_tasks()

    pending = [
        task for task in tasks
        if not task[4]
    ]

    priority_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2
    }

    pending.sort(
        key=lambda task: (
            task[2],
            priority_order.get(task[3], 3)
        )
    )

    return pending


# Generate a study plan
def create_study_plan(
    selected_date,
    start,
    end,
    study_hours
):

    db.initialize_database()

    tasks = get_prioritized_tasks()

    free_slots = get_free_slots(
        selected_date, start, end
    )

    remaining = int(study_hours * 60)

    plan = []

    task_index = 0

    for slot_start, slot_end in free_slots:

        current = slot_start

        while (
            current < slot_end
            and remaining > 0
            and task_index < len(tasks)
        ):

            duration = min(
                60,
                slot_end - current,
                remaining
            )

            # Avoid very short sessions
            if duration < 15:
                break

            task = tasks[task_index]

            plan.append({
                "task_id": task[0],
                "task": task[1],
                "priority": task[3],
                "deadline": task[2],
                "start": to_clock(current),
                "end": to_clock(
                    current + duration
                ),
                "duration": duration
            })

            current += duration

            remaining -= duration

            task_index += 1

        if remaining <= 0:
            break

    return plan


# Independently verify the study plan
def verify_plan(
    plan,
    selected_date,
    start,
    end
):

    classes = get_daily_classes(selected_date)

    pending_ids = {
        task[0]
        for task in get_prioritized_tasks()
    }

    problems = []

    available_start = to_minutes(start)
    available_end = to_minutes(end)

    previous_end = available_start

    for session in plan:

        study_start = to_minutes(
            session["start"]
        )

        study_end = to_minutes(
            session["end"]
        )

        if study_end <= study_start:

            problems.append(
                "Invalid session duration."
            )

        if (
            study_start < available_start
            or study_end > available_end
        ):

            problems.append(
                "Session outside available hours."
            )

        if study_start < previous_end:

            problems.append(
                "Study sessions overlap."
            )

        previous_end = study_end

        if session["task_id"] not in pending_ids:

            problems.append(
                "Task is completed or missing."
            )

        for item in classes:

            class_start = to_minutes(item[3])
            class_end = to_minutes(item[4])

            if (
                study_start < class_end
                and study_end > class_start
            ):

                problems.append(
                    f"Conflict with {item[1]}"
                )

    return len(problems) == 0, problems
