from flask import Flask, render_template, request, jsonify
from database import init_db
from services.task_service import add_task

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
        task_title = message.strip[3:].strip() 
        
        if task_title:
            add_task(task_title) 
            return jsonify({"response": f"Got it! I added '{task_title}' to your task list."})
        else:
            return jsonify({"response": "What would you like me to add?"})

    
    return jsonify({
    "response": f"You said: {message}. I'm still learning! For now, try commands like 'add buy milk'."
})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)