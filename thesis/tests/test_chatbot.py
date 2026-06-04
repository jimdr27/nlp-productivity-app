import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot.chatbot_engine import parse_message

def test_add_task_basic():
    result = parse_message("add buy groceries")
    assert result["intent"] == "add_task"
    assert result["task_title"] is not None

def test_add_task_with_remind():
    result = parse_message("remind me to call mom")
    assert result["intent"] == "add_task"

def test_add_task_with_date():
    result = parse_message("add dentist appointment tomorrow")
    assert result["intent"] == "add_task"
    assert result["due_date"] is not None

def test_show_tasks():
    result = parse_message("show my tasks")
    assert result["intent"] == "show_tasks"

def test_list_tasks():
    result = parse_message("list tasks")
    assert result["intent"] == "show_tasks"

def test_complete_task():
    result = parse_message("complete task 3")
    assert result["intent"] == "complete_task"
    assert result["task_id"] == 3

def test_finish_task():
    result = parse_message("I finished task 2")
    assert result["intent"] == "complete_task"
    assert result["task_id"] == 2

def test_delete_task():
    result = parse_message("delete task 4")
    assert result["intent"] == "delete_task"
    assert result["task_id"] == 4

def test_unknown_intent():
    result = parse_message("hello there")
    assert result["intent"] == "unknown"

def test_today_intent():
    result = parse_message("what tasks do I have today")
    assert result["intent"] == "tasks_today"