from flask import Blueprint, request, jsonify
from datetime import datetime
from services.task_service import add_task, get_tasks, complete_task, delete_task
from chatbot.chatbot_engine import parse_message
import dateparser

task_bp = Blueprint("tasks", __name__)

@task_bp.route("/test-nlp", methods=["POST"])
def test_nlp():
    data = request.get_json()
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "No message provided"}), 400
    parsed = parse_message(message)
    return jsonify({"original": message, "parsed": parsed})


@task_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({"response": "Please type something!"})

    parsed_data = parse_message(message)
    intent = parsed_data["intent"]

    # ADD TASK
    if intent == "add_task":
        task_title = parsed_data["task_title"]
        due_date = parsed_data["due_date"]

        if task_title:
            add_task(task_title, due_date=due_date)
            date_msg = ""
            if due_date:
                try:
                    formatted = datetime.strptime(due_date, "%Y-%m-%d %H:%M").strftime("%d %b at %H:%M")
                    date_msg = f" Due: {formatted}."
                except:
                    date_msg = f" Due: {due_date}."
            return jsonify({
                "response": f"Got it! I added '{task_title}' to your task list.{date_msg}"
            })

        return jsonify({"response": "I understood you want to add a task, but what exactly should I add?"})

    # SHOW TASKS
    elif intent == "show_tasks":
        tasks = get_tasks()
        if not tasks:
            return jsonify({"response": "You have no pending tasks! Great job."})

        lines = []
        task_data_list = []
        for task in tasks:
            line = f"• [ID: {task.id}] {task.title}"
            if task.due_date:
                try:
                    parsed = dateparser.parse(task.due_date)
                    formatted = parsed.strftime("%d %b %H:%M") if parsed else task.due_date
                except:
                    formatted = task.due_date
                line += f" (Due: {formatted})"
            lines.append(line)
            task_data_list.append({"id": task.id, "title": task.title})

        return jsonify({
            "response": "Here are your tasks:<br>" + "<br>".join(lines),
            "tasks": task_data_list
        })

    # TODAY
    elif intent == "tasks_today":
        today = datetime.now().strftime("%Y-%m-%d")
        tasks = [t for t in get_tasks() if t.due_date and t.due_date.startswith(today)]
        if not tasks:
            return jsonify({"response": "No tasks due today! Great job."})
        return jsonify({
            "response": "Tasks due today:<br>" + "<br>".join([f"• [ID: {t.id}] {t.title}" for t in tasks])
        })

    # COMPLETE
    elif intent == "complete_task":
        task_id = parsed_data["task_id"]
        if task_id is not None:
            if complete_task(task_id):
                return jsonify({"response": f"Task {task_id} completed!"})
            return jsonify({"response": f"I couldn't find a task with ID {task_id}."})
        return jsonify({"response": "Which task ID would you like to complete? (e.g., 'complete task 2')"})

    # DELETE
    elif intent == "delete_task":
        task_id = parsed_data["task_id"]
        if task_id is not None:
            if delete_task(task_id):
                return jsonify({"response": f"Task {task_id} deleted."})
            return jsonify({"response": f"I couldn't find a task with ID {task_id}."})
        return jsonify({"response": "Which task ID would you like to delete? (e.g., 'delete task 3')"})

    return jsonify({
        "response": f"I'm not quite sure what you mean by '{message}'. Try: add, show, complete, or delete."
    })