
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "student_assistant.db"


def connect_db():
    DATA_DIR.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            due_date TEXT NOT NULL,
            priority TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            day TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            room TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_task(name, due_date, priority):
    connection = connect_db()

    connection.execute(
        "INSERT INTO tasks (name, due_date, priority) VALUES (?, ?, ?)",
        (name, str(due_date), priority)
    )

    connection.commit()
    connection.close()


def get_tasks():
    connection = connect_db()

    tasks = connection.execute(
        "SELECT * FROM tasks ORDER BY due_date"
    ).fetchall()

    connection.close()
    return tasks


def update_task_status(task_id, done):
    connection = connect_db()

    connection.execute(
        "UPDATE tasks SET done = ? WHERE id = ?",
        (int(done), task_id)
    )

    connection.commit()
    connection.close()


def delete_task(task_id):
    connection = connect_db()

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()


def add_class(subject, day, start_time, end_time, room):
    connection = connect_db()

    connection.execute("""
        INSERT INTO classes
        (subject, day, start_time, end_time, room)
        VALUES (?, ?, ?, ?, ?)
    """, (subject, day, str(start_time), str(end_time), room))

    connection.commit()
    connection.close()


def get_classes():
    connection = connect_db()

    classes = connection.execute(
        "SELECT * FROM classes"
    ).fetchall()

    connection.close()
    return classes


def delete_class(class_id):
    connection = connect_db()

    connection.execute(
        "DELETE FROM classes WHERE id = ?",
        (class_id,)
    )

    connection.commit()
    connection.close()
