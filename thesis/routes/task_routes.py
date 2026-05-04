from flask import Blueprint, request, jsonify
from services.task_service import add_task, get_tasks, complete_task
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

    if intent == "add_task":
        task_title = parsed_data["task_title"]
        if task_title:
            add_task(task_title, due_date=None)
            return jsonify({"response": f"Got it! I added '{task_title}' to your task list."})
        else:
            return jsonify({"response": "I understood you want to add a task, but what exactly should I add?"})

    elif intent == "show_tasks":
        tasks = get_tasks()
        if not tasks:
            return jsonify({"response": "You have no pending tasks! Great job."})
        task_list = "<br>".join([f"• [ID: {task['id']}] {task['title']}" for task in tasks])
        return jsonify({"response": f"Here are your tasks:<br>{task_list}"})

    elif intent == "complete_task":
        task_id = parsed_data["task_id"]
        if task_id is not None:
            success = complete_task(task_id)
            if success:
                return jsonify({"response": f"Task {task_id} completed!"})
            else:
                return jsonify({"response": f"I couldn't find a task with ID {task_id}."})
        else:
            return jsonify({"response": "Which task ID would you like to complete? (e.g., 'complete task 2')"})

    return jsonify({
        "response": f"I'm not quite sure what you mean by '{message}'. Try asking me to add a task, list your tasks, or complete a task."
    })

