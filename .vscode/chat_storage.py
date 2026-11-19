
from database import connect_db


def initialize_chat_storage():

    conn = connect_db()

    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ai_chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()

    finally:
        conn.close()


def save_message(role, content):

    conn = connect_db()

    try:
        conn.execute("""
            INSERT INTO ai_chat_messages (role, content)
            VALUES (?, ?)
        """, (role, content))

        conn.commit()

    finally:
        conn.close()


def get_chat_history():

    conn = connect_db()

    try:
        rows = conn.execute("""
            SELECT role, content
            FROM ai_chat_messages
            ORDER BY id ASC
        """).fetchall()

        return [
            {
                "role": row[0],
                "content": row[1]
            }
            for row in rows
        ]

    finally:
        conn.close()


def clear_chat_history():

    conn = connect_db()

    try:
        conn.execute("DELETE FROM ai_chat_messages")
        conn.commit()

    finally:
        conn.close()

