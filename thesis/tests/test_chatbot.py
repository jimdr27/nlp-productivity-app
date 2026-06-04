from chatbot.chatbot_engine import parse_message


def test_add_task_intent():
    result = parse_message("add buy milk")

    assert result["intent"] == "add_task"
    assert "buy milk" in result["task_title"].lower()


def test_show_tasks_intent():
    result = parse_message("show my tasks")

    assert result["intent"] == "show_tasks"


def test_complete_task_intent():
    result = parse_message("complete task 5")

    assert result["intent"] == "complete_task"
    assert result["task_id"] == 5


def test_delete_task_intent():
    result = parse_message("delete task 2")

    assert result["intent"] == "delete_task"
    assert result["task_id"] == 2