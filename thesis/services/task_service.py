from database import get_connection

def add_task(title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title) VALUES (?)",
        (title,)
    )

    conn.commit()
    conn.close()

def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, title 
    FROM tasks 
    WHERE status = 'pending'
    ORDER BY id DESC
    """)
    tasks = cursor.fetchall()

    conn.close()
    return tasks