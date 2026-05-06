import sqlite3
from contextlib import contextmanager
from config import DB_PATH

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                due_date TEXT,
                status TEXT DEFAULT 'pending'
                CHECK(status IN ('pending', 'completed'))
            )
        """)

    print("Database initialized successfully!")


if __name__ == "__main__":
    init_db()
    