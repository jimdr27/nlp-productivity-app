from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    # This serves the frontend UI
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # This catches the message from the frontend
    data = request.get_json()
    message = data.get("message")
    
    # For now, just echo it back. We will add spaCy here later!
    return jsonify({"response": f"You said: {message}"})

if __name__ == "__main__":
    app.run(debug=True)