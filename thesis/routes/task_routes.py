from flask import Blueprint, request, jsonify
from datetime import datetime
from services.task_service import add_task, get_tasks, complete_task, delete_task
from chatbot.chatbot_engine import parse_message

task_bp = Blueprint("tasks", __name__)


@task_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({"response": "Please type something!"})

    parsed_data = parse_message(message)
    intent = parsed_data["intent"]

    #  ADD TASK
    if intent == "add_task":
        task_title = parsed_data["task_title"]
        due_date = parsed_data["due_date"]

        if task_title:
            add_task(task_title, due_date=due_date)

            date_msg = ""
            if due_date:
                try:
                    formatted = datetime.strptime(due_date, "%Y-%m-%d %H:%M") \
                                        .strftime("%d %b at %H:%M")
                    date_msg = f" Due: {formatted}."
                except:
                    date_msg = f" Due: {due_date}."

            return jsonify({
                "response": f"Got it! I added '{task_title}' to your task list.{date_msg}"
            })

        return jsonify({"response": "What should I add?"})

    #  SHOW TASKS
    elif intent == "show_tasks":
        tasks = get_tasks()

        if not tasks:
            return jsonify({"response": "You have no pending tasks! 🎉"})

        lines = []
        for task in tasks:
            line = f"• [ID: {task['id']}] {task['title']}"

            if task["due_date"]:
                try:
                    formatted = datetime.strptime(task["due_date"], "%Y-%m-%d %H:%M") \
                                        .strftime("%d %b %H:%M")
                    line += f" (Due: {formatted})"
                except:
                    line += f" (Due: {task['due_date']})"

            lines.append(line)

        return jsonify({
            "response": "Here are your tasks:<br>" + "<br>".join(lines)
        })

    #  TODAY
    elif intent == "tasks_today":
        today = datetime.now().strftime("%Y-%m-%d")

        tasks = [
            t for t in get_tasks()
            if t["due_date"] and t["due_date"].startswith(today)
        ]

        if not tasks:
            return jsonify({"response": "No tasks due today 🎉"})

        return jsonify({
            "response": "Tasks due today:<br>" +
                        "<br>".join([f"• {t['title']}" for t in tasks])
        })

    #  COMPLETE
    elif intent == "complete_task":
        task_id = parsed_data["task_id"]

        if task_id is not None:
            if complete_task(task_id):
                return jsonify({"response": f"Task {task_id} completed!"})
            return jsonify({"response": "Task not found."})

        return jsonify({"response": "Please specify task ID."})

    #  DELETE
    elif intent == "delete_task":
        task_id = parsed_data["task_id"]

        if task_id is not None:
            if delete_task(task_id):
                return jsonify({"response": f"Task {task_id} deleted."})
            return jsonify({"response": "Task not found."})

        return jsonify({"response": "Please specify task ID."})

    return jsonify({
        "response": f"I didn't understand '{message}'. Try add/show/complete/delete."
    })
