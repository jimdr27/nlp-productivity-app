from flask import Flask, render_template, request, jsonify
from database import init_db
from services.task_service import add_task, get_tasks

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
    
    
    if clean_message.startswith("add"):  
        
        task_title = message.strip()[4:].strip() 
        
        if task_title:
            add_task(task_title) 
            return jsonify({"response": f"Got it! I added '{task_title}' to your task list."})
        else:
            return jsonify({"response": "What would you like me to add?"})
            
    
    elif clean_message.startswith("show"):
        tasks = get_tasks()

        if not tasks:
            return jsonify({"response": "You have no pending tasks! Great job."})

        
        task_list = "<br>".join([f"• {task['title']}" for task in tasks])
        return jsonify({"response": f"Here are your tasks:<br>{task_list}"})

    
    return jsonify({
        "response": f"You said: {message}. I'm still learning! Try typing 'add [task]' or 'show tasks'."
    })

if __name__ == "__main__":
    init_db()
    app.run(debug=True)