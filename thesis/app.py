from flask import Flask, render_template, request, jsonify
from database import init_db
from services.task_service import add_task, get_tasks, complete_task

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message")
    
    if not message:
        return jsonify({"response": "Please type something!"})
    
    clean_message = message.lower().strip()
    
    # ➕ ADD TASK
    if clean_message.startswith("add "):  
        task_title = clean_message[4:].strip()
        
        if task_title:
            add_task(task_title, due_date=None) 
            return jsonify({
                "response": f"Got it! I added '{task_title}' to your task list."
            })
        else:
            return jsonify({"response": "What would you like me to add?"})
    
    # 📋 SHOW TASKS
    elif clean_message.startswith("show"):
        tasks = get_tasks()

        if not tasks:
            return jsonify({"response": "You have no pending tasks! Great job."})

        task_list = "<br>".join([f"• [ID: {task['id']}] {task['title']}" for task in tasks])
        return jsonify({"response": f"Here are your tasks:<br>{task_list}"})
    
    # ✅ COMPLETE TASK
    elif clean_message.startswith("complete task"):
        task_id = clean_message.replace("complete task", "", 1).strip()

        if task_id.isdigit():
            success = complete_task(int(task_id))
            if success:
                return jsonify({"response": "Task completed!"})
            else:
                return jsonify({"response": "Task not found."})
        else:
            return jsonify({"response": "Please provide a valid task ID."})

    # 🤖 DEFAULT RESPONSE
    return jsonify({
        "response": f"You said: {message}. I'm still learning! Try 'add buy milk' or 'show tasks'."
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)  

