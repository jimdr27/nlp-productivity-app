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

    # ➕ ADD TASK
    if intent == "add_task":
        task_title = parsed_data["task_title"]
        due_date = parsed_data["due_date"]

        if task_title:
            add_task(task_title, due_date=due_date)

            if due_date:
                try:
                    formatted_date = datetime.strptime(due_date, "%Y-%m-%d %H:%M") \
                                              .strftime("%d %b at %H:%M")
                    date_msg = f" Due: {formatted_date}."
                except:
                    date_msg = f" Due: {due_date}."
            else:
                date_msg = ""

            return jsonify({
                "response": f"Got it! I added '{task_title}' to your task list.{date_msg}"
            })
        else:
            return jsonify({
                "response": "I understood you want to add a task, but what exactly should I add?"
            })

    # 📋 SHOW TASKS
    elif intent == "show_tasks":
        tasks = get_tasks()

        if not tasks:
            return jsonify({"response": "You have no pending tasks! Great job."})

        task_lines = []
        for task in tasks:
            line = f"• [ID: {task['id']}] {task['title']}"

            if task["due_date"]:
                try:
                    formatted_date = datetime.strptime(task["due_date"], "%Y-%m-%d %H:%M") \
                                              .strftime("%d %b %H:%M")
                    line += f" (Due: {formatted_date})"
                except:
                    line += f" (Due: {task['due_date']})"

            task_lines.append(line)

        task_list = "<br>".join(task_lines)

        return jsonify({"response": f"Here are your tasks:<br>{task_list}"})


    # 📅 TASKS DUE TODAY
    elif intent == "tasks_today":
        today = datetime.now().strftime("%Y-%m-%d")

        tasks = [
            task for task in get_tasks()
            if task["due_date"] and task["due_date"].startswith(today)
        ]

        if not tasks:
            return jsonify({"response": "No tasks due today 🎉"})

        task_list = "<br>".join([f"• {task['title']}" for task in tasks])
        return jsonify({"response": f"Tasks due today:<br>{task_list}"})


    # ✅ COMPLETE TASK
    elif intent == "complete_task":
        task_id = parsed_data["task_id"]

        if task_id is not None:
            success = complete_task(task_id)

            if success:
                return jsonify({"response": f"Task {task_id} completed!"})
            else:
                return jsonify({"response": f"I couldn't find a task with ID {task_id}."})
        else:
            return jsonify({
                "response": "Which task ID would you like to complete? (e.g., 'complete task 2')"
            })

    # ❌ DELETE TASK
    elif intent == "delete_task":
        task_id = parsed_data["task_id"]
        if task_id is not None:
            success = delete_task(task_id)
            if success:
                return jsonify({"response": f"Task {task_id} deleted."})
            else:
                return jsonify({"response": f"I couldn't find a task with ID {task_id}."})
        else:
            return jsonify({"response": "Which task ID would you like to delete? (e.g., 'delete task 3')"})


    # 🤖 DEFAULT
    return jsonify({
        "response": f"I'm not quite sure what you mean by '{message}'. Try: add, show, complete, or 'today'."
    })
