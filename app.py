from flask import Flask, render_template, request, jsonify
import json
import os
import random
import string
from datetime import datetime

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

# Trasa do generatora haseł
@app.route("/password")
@app.route("/password/")
def password_page():
    return render_template("password.html")

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

# Funkcja do generowania hasła
def generate_password(length, include_uppercase, include_special, include_digits):
    if length < 4:
        return {"error": "Password length must be at least 4 characters."}

    lower = string.ascii_lowercase
    uppercase = string.ascii_uppercase if include_uppercase else ""
    special = string.punctuation if include_special else ""
    digits = string.digits if include_digits else ""
    all_characters = lower + uppercase + special + digits

    if not all_characters:
        return {"error": "You must select at least one character type."}

    required_characters = []
    if include_uppercase:
        required_characters.append(random.choice(uppercase))
    if include_special:
        required_characters.append(random.choice(special))
    if include_digits:
        required_characters.append(random.choice(digits))

    remaining_length = length - len(required_characters)
    password = required_characters + [random.choice(all_characters) for _ in range(remaining_length)]
    random.shuffle(password)

    return {"password": "".join(password)}

# API do generowania hasła
@app.route("/api/generate_password", methods=["POST"])
def generate_password_api():
    data = request.json
    length = data.get("length", 8)
    include_uppercase = data.get("include_uppercase", False)
    include_special = data.get("include_special", False)
    include_digits = data.get("include_digits", False)

    result = generate_password(length, include_uppercase, include_special, include_digits)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
