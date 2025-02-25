from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

file_name = "base/todo_list.json"

# Tworzy folder "base", jeśli nie istnieje
os.makedirs("base", exist_ok=True)

# Funkcje do obsługi zadań
def load_tasks():
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except:
        return {"tasks": []}

def save_tasks(tasks):
    try:
        with open(file_name, "w") as file:
            json.dump(tasks, file)
    except:
        print("Failed to save.")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/todo")
@app.route("/todo/")
def todo_page():
    return render_template("todo.html")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)

@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.json
    tasks = load_tasks()
    new_task = {
        "description": data["description"],
        "complete": False,
        "create_time": datetime.now().strftime('%d-%m-%Y %H:%M')
    }
    tasks["tasks"].append(new_task)
    save_tasks(tasks)
    return jsonify({"message": "Task added.", "task": new_task}), 201

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks["tasks"]):
        deleted_task = tasks["tasks"].pop(task_id)
        save_tasks(tasks)
        return jsonify({"message": "Task deleted.", "task": deleted_task})
    return jsonify({"error": "Invalid task ID"}), 400

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks["tasks"]):
        tasks["tasks"][task_id]["complete"] = not tasks["tasks"][task_id]["complete"]
        save_tasks(tasks)
        return jsonify({"message": "Task updated.", "task": tasks["tasks"][task_id]})
    return jsonify({"error": "Invalid task ID"}), 400

if __name__ == "__main__":
    app.run(debug=True)
