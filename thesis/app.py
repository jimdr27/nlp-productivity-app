from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Flask!"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message")

    return jsonify({"response": f"You said: {message}"})


if __name__ == "__main__":
    app.run(debug=True)