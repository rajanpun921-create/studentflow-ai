import json
from datetime import datetime
import database as db


# Create the approved plans table
def initialize_plan_storage():

    connection = db.connect_db()

    try:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS approved_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                study_date TEXT NOT NULL,
                available_from TEXT NOT NULL,
                available_until TEXT NOT NULL,
                requested_hours INTEGER NOT NULL,
                total_minutes INTEGER NOT NULL,
                plan_json TEXT NOT NULL,
                approved_at TEXT NOT NULL
            )
        """)

        connection.commit()

    finally:

        connection.close()


# Save an approved study plan
def save_approved_plan(plan, settings):

    initialize_plan_storage()

    connection = db.connect_db()

    total_minutes = sum(
        item["duration"] for item in plan
    )

    try:

        cursor = connection.execute("""
            INSERT INTO approved_plans (
                study_date,
                available_from,
                available_until,
                requested_hours,
                total_minutes,
                plan_json,
                approved_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(settings["date"]),
            str(settings["start"]),
            str(settings["end"]),
            settings["hours"],
            total_minutes,
            json.dumps(plan),
            datetime.now().isoformat(
                timespec="seconds"
            )
        ))

        connection.commit()

        return cursor.lastrowid

    finally:

        connection.close()


# Retrieve all approved plans
def get_saved_plans():

    initialize_plan_storage()

    connection = db.connect_db()

    connection.row_factory = __import__(
        "sqlite3"
    ).Row

    try:

        rows = connection.execute("""
            SELECT *
            FROM approved_plans
            ORDER BY study_date DESC, id DESC
        """).fetchall()

        plans = []

        for row in rows:

            item = dict(row)

            item["sessions"] = json.loads(
                item["plan_json"]
            )

            plans.append(item)

        return plans

    finally:

        connection.close()


# Delete or withdraw a saved plan
def delete_saved_plan(plan_id):

    connection = db.connect_db()

    try:

        connection.execute("""
            DELETE FROM approved_plans
            WHERE id = ?
        """, (plan_id,))

        connection.commit()

    finally:

        connection.close()
