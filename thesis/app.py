from flask import Flask, render_template, request, jsonify
from database import init_db

app = Flask(__name__)

@app.route("/")
def home():
    
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    
    data = request.get_json()
    message = data.get("message")
    
    
    return jsonify({"response": f"You said: {message}"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)