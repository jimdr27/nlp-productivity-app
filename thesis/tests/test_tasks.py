import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import database
from services.task_service import add_task, get_tasks, complete_task, delete_task

@pytest.fixture(autouse=True)
def use_test_db(tmp_path, monkeypatch):
    """Each test gets a fresh temporary database."""
    test_db = str(tmp_path / "test.db")
    monkeypatch.setattr(database, "DB_PATH", test_db)
    database.init_db()

def test_add_and_get_task():
    add_task("Buy milk")
    tasks = get_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Buy milk"

def test_add_task_with_due_date():
    add_task("Dentist", due_date="2025-12-01 10:00")
    tasks = get_tasks()
    assert tasks[0].due_date == "2025-12-01 10:00"

def test_complete_task():
    add_task("Read book")
    tasks = get_tasks()
    task_id = tasks[0].id
    result = complete_task(task_id)
    assert result is True
    assert get_tasks() == []  # no more pending tasks

def test_complete_nonexistent_task():
    result = complete_task(9999)
    assert result is False

def test_delete_task():
    add_task("Go running")
    tasks = get_tasks()
    task_id = tasks[0].id
    result = delete_task(task_id)
    assert result is True
    assert get_tasks() == []

def test_delete_nonexistent_task():
    result = delete_task(9999)
    assert result is False

def test_multiple_tasks_ordered():
    add_task("First task")
    add_task("Second task")
    tasks = get_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Second task"  # ORDER BY id DESC