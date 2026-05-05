from flask import Flask, render_template
from database import init_db
from routes.task_routes import task_bp

app = Flask(__name__)
app.config.from_pyfile("config.py")

app.register_blueprint(task_bp)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=app.config["DEBUG"])
    