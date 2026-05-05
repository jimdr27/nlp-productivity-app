from database import get_connection

def add_task(task_title, due_date=None):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO tasks (title, due_date) VALUES (?, ?)",
            (task_title, due_date)
        )
        conn.commit()


def get_tasks():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, title, due_date, status
            FROM tasks
            WHERE status = 'pending'
            ORDER BY id DESC
        """).fetchall()

        return [dict(row) for row in rows]


def complete_task(task_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET status = 'done' WHERE id = ?",
            (task_id,)
        )
        conn.commit()
        return cursor.rowcount > 0


def delete_task(task_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    