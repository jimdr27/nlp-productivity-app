from database import get_connection

def add_task(task_title, due_date=None):
    conn = get_connection()
    conn.execute(
        "INSERT INTO tasks (title, due_date) VALUES (?, ?)",
        (task_title, due_date)
    )
    conn.commit()
    conn.close()


def get_tasks():
    conn = get_connection()
    rows = conn.execute("""
        SELECT id, title, due_date, status
        FROM tasks
        WHERE status = 'pending'
        ORDER BY id DESC
    """).fetchall()
    conn.close()

    return [dict(row) for row in rows]


def complete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET status = 'done' WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()

    return updated > 0

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    
    return deleted > 0
