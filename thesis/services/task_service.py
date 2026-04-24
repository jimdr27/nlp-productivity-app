from database import get_connection

def add_task(task_title, due_date=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, due_date) VALUES (?, ?)",
        (task_title, due_date)
    )
    conn.commit()
    conn.close()

def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, due_date, status
        FROM tasks
        WHERE status = 'pending'
        ORDER BY id DESC
    """)
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return tasks

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
