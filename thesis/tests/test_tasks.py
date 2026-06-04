from services.task_service import (
    add_task,
    get_tasks,
    complete_task,
    delete_task
)


def test_add_task():
    task_id = add_task("Test Task")

    assert isinstance(task_id, int)


def test_get_tasks():
    tasks = get_tasks()

    assert isinstance(tasks, list)


def test_complete_task():
    task_id = add_task("Complete Me")

    success = complete_task(task_id)

    assert success is True


def test_delete_task():
    task_id = add_task("Delete Me")

    success = delete_task(task_id)

    assert success is True