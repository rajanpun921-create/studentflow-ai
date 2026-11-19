
from datetime import date, time

from planner import (
    create_study_plan,
    verify_plan,
    get_daily_classes,
    get_free_slots,
    to_clock
)

selected_date = date(2026, 11, 19)

start = time(9, 0)
end = time(18, 0)

study_hours = 3

print("=" * 45)
print("INTELLIGENT STUDY PLANNER")
print("=" * 45)

print("\nSelected date:", selected_date)

print("\nScheduled classes:")

for item in get_daily_classes(selected_date):

    print(
        item[1],
        item[3][:5],
        "-",
        item[4][:5]
    )

print("\nAvailable study periods:")

for slot in get_free_slots(
    selected_date, start, end
):

    print(
        to_clock(slot[0]),
        "-",
        to_clock(slot[1])
    )

plan = create_study_plan(
    selected_date,
    start,
    end,
    study_hours
)

print("\nGenerated Study Plan:")

for session in plan:

    print(
        session["start"],
        "-",
        session["end"],
        "|",
        session["task"],
        "|",
        session["priority"]
    )

total = sum(
    item["duration"] for item in plan
)

print("\nTotal study minutes:", total)

valid, problems = verify_plan(
    plan,
    selected_date,
    start,
    end
)

print("\nVerification Result:")

if not plan:

    print("No study sessions could be generated.")

elif valid:

    print("PASS: No schedule conflicts.")

else:

    print("FAIL:", problems)

if total < study_hours * 60:

    print("Requested study duration not fully met.")

# Test a deliberately conflicting session
if plan:

    bad_plan = [dict(plan[0])]

    bad_plan[0]["start"] = "10:15"
    bad_plan[0]["end"] = "11:15"

    valid, problems = verify_plan(
        bad_plan,
        selected_date,
        start,
        end
    )

    print("\nIntentional Conflict Test:")

    if not valid:

        print("PASS: Conflict successfully detected.")

        print(problems)

    else:

        print("FAIL: Conflict was not detected.")
