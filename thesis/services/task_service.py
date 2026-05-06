from database import get_connection
from models.task import Task
from typing import List, Optional

def add_task(task_title: str, due_date: Optional[str] = None) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, due_date) VALUES (?, ?)",
            (task_title, due_date)
        )
        return cursor.lastrowid


def get_tasks() -> List[Task]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, title, due_date, status
            FROM tasks
            WHERE status = 'pending'
            ORDER BY id DESC
        """).fetchall()

        return [Task(**dict(row)) for row in rows]


def complete_task(task_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE tasks SET status = 'completed' WHERE id = ?",
            (task_id,)
        )
        return cursor.rowcount > 0


def delete_task(task_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )
        return cursor.rowcount > 0
    