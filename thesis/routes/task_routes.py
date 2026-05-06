from flask import Blueprint, request, jsonify
from datetime import datetime
from services.task_service import add_task, get_tasks, complete_task, delete_task
from chatbot.chatbot_engine import parse_message

task_bp = Blueprint("tasks", __name__)


@task_bp.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({"response": "Please type something!"})

    parsed = parse_message(message)
    intent = parsed["intent"]

    # ➕ ADD TASK
    if intent == "add_task":
        title = parsed["task_title"]
        due = parsed["due_date"]

        if not title:
            return jsonify({"response": "What should I add?"})

        add_task(title, due)

        date_msg = ""
        if due:
            try:
                formatted = datetime.strptime(due, "%Y-%m-%d %H:%M") \
                                    .strftime("%d %b at %H:%M")
                date_msg = f" Due: {formatted}."
            except:
                date_msg = f" Due: {due}."

        return jsonify({
            "response": f"Got it! I added '{title}'.{date_msg}"
        })

    # 📋 SHOW TASKS
    elif intent == "show_tasks":
        tasks = get_tasks()

        if not tasks:
            return jsonify({"response": "You have no pending tasks! 🎉"})

        lines = []
        for t in tasks:
            line = f"• [ID: {t.id}] {t.title}"

            if t.due_date:
                try:
                    formatted = datetime.strptime(t.due_date, "%Y-%m-%d %H:%M") \
                                        .strftime("%d %b %H:%M")
                    line += f" (Due: {formatted})"
                except:
                    line += f" (Due: {t.due_date})"

            lines.append(line)

        return jsonify({
            "response": "Here are your tasks:<br>" + "<br>".join(lines)
            
        })

    # 📅 TASKS DUE TODAY
    elif intent == "tasks_today":
        today = datetime.now().strftime("%Y-%m-%d")

        tasks = [
            t for t in get_tasks()
            if t.due_date and t.due_date.startswith(today)
        ]

        if not tasks:
            return jsonify({"response": "No tasks due today 🎉"})

        return jsonify({
            "response": "Today's tasks:<br>" +
                        "<br>".join([f"• {t.title}" for t in tasks])
        })

    # ✅ COMPLETE TASK
    elif intent == "complete_task":
        task_id = parsed["task_id"]

        if task_id is None:
            return jsonify({
                "response": "Which task ID would you like to complete? (e.g., 'complete task 2')"
            })

        if complete_task(task_id):
            return jsonify({"response": f"Task {task_id} completed!"})

        return jsonify({"response": f"I couldn't find a task with ID {task_id}."})

    # ❌ DELETE TASK
    elif intent == "delete_task":
        task_id = parsed["task_id"]

        if task_id is None:
            return jsonify({
                "response": "Which task ID would you like to delete? (e.g., 'delete task 3')"
            })

        if delete_task(task_id):
            return jsonify({"response": f"Task {task_id} deleted."})

        return jsonify({"response": f"I couldn't find a task with ID {task_id}."})

    # 🤖 DEFAULT FALLBACK
    return jsonify({
        "response": f"I didn't understand '{message}'. Try: add, show, complete, delete, or 'today'."
    })
