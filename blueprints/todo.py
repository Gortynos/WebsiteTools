import json
from datetime import datetime

from flask import Blueprint, current_app, jsonify, request
from extensions import limiter
from i18n import t

todo_bp = Blueprint("todo_api", __name__)


def load_tasks():
    tasks_file = current_app.config["TASKS_FILE"]
    try:
        with open(tasks_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        current_app.logger.warning("Task file missing or invalid JSON, using empty list.")
        return {"tasks": []}
    except OSError:
        current_app.logger.exception("Failed to read task file: %s", tasks_file)
        return {"tasks": []}


def save_tasks(tasks):
    tasks_file = current_app.config["TASKS_FILE"]
    try:
        with open(tasks_file, "w", encoding="utf-8") as file:
            json.dump(tasks, file)
    except OSError:
        current_app.logger.exception("Failed to save tasks to file: %s", tasks_file)


@todo_bp.route("/api/tasks", methods=["GET"])
@limiter.limit("120 per minute")
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)


@todo_bp.route("/api/tasks", methods=["POST"])
@limiter.limit("30 per minute")
def add_task():
    data = request.json or {}
    description = data.get("description", "").strip()
    if not description:
        return jsonify({"error": t("todo.description_required")}), 400

    tasks = load_tasks()
    new_task = {
        "description": description,
        "complete": False,
        "create_time": datetime.now().strftime("%d-%m-%Y %H:%M"),
    }
    tasks["tasks"].append(new_task)
    save_tasks(tasks)
    return jsonify({"message": t("todo.task_added"), "task": new_task}), 201


@todo_bp.route("/api/tasks/<int:task_id>", methods=["DELETE"])
@limiter.limit("30 per minute")
def delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks["tasks"]):
        deleted_task = tasks["tasks"].pop(task_id)
        save_tasks(tasks)
        return jsonify({"message": t("todo.task_deleted"), "task": deleted_task})
    return jsonify({"error": t("todo.invalid_task_id")}), 400


@todo_bp.route("/api/tasks/<int:task_id>", methods=["PUT"])
@limiter.limit("30 per minute")
def update_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks["tasks"]):
        tasks["tasks"][task_id]["complete"] = not tasks["tasks"][task_id]["complete"]
        save_tasks(tasks)
        return jsonify({"message": t("todo.task_updated"), "task": tasks["tasks"][task_id]})
    return jsonify({"error": t("todo.invalid_task_id")}), 400
