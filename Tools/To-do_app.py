import json
from datetime import datetime

file_name = "base\todo_list.json"

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

def view_tasks(tasks):
    print()
    task_list = tasks["tasks"]
    if len(task_list) == 0:
        print("No tasks to display.")
    else:
        print("Your To-Do List: ")
        for i, task in enumerate(task_list):
            if task["complete"]:
                status = "[Completed]"
            elif task["complete"] == None:
                status = "[Not completed]"
            else:
                status = "[In process]"
            print(f"{i + 1}. {task['description']} | {status} | Created: {task['create_time']}")

def create_task(tasks):
    description = input("Enter the task description: ").strip()
    if description:
        tasks["tasks"].append({"description": description, "complete": False, "create_time" : datetime.now().strftime('%d-%m-%Y %H:%M')})
        save_tasks(tasks)
        print("Task added.")
    else:
        print("Description cannot be empty.")

def mark_task_complete(tasks):
    view_tasks(tasks)
    try:
        task_number = int(input("Enter the task number to mark as complete: ").strip())
        if 0 <= task_number and 0 < len(tasks):
            tasks["tasks"][task_number - 1]["complete"] = True
            save_tasks(tasks)
            print("Task marked as complete.")
        else:
            print("Invalid task number.")
    except:
        print("Enter a valid number.")

def delete_task(tasks):
    view_tasks(tasks)
    try:
        task_number = int(input("Enter the task number to delete: ").strip())
        if 0 <= task_number and 0 < len(tasks):
            tasks["tasks"].pop(task_number - 1)
            save_tasks(tasks)
            print("The task has been deleted.")
        else:
            print("Invalid task number.")
    except:
        print("Enter a valid number.")

def mark_task_incomplete(tasks):
    view_tasks(tasks)
    try:
        task_number = int(input("Enter the task number to mark as incomplete: ").strip())
        if 0 < task_number and 0 < len(tasks):
            tasks["tasks"][task_number - 1]["complete"] = None
            save_tasks(tasks)
            print("Task marked as incomplete.")
        else:
            print("Invalid task number.")
    except:
        print("Enter a valid number.")

def run_todo_manager():
    tasks = load_tasks()

    while True:
        print("\nTo-Do List Manager")
        print("1. View tasks")
        print("2. Add task")
        print("3. Mark complete task")
        print("4. Delete task")
        print("5. Mark as incomplete")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            create_task(tasks)
        elif choice == "3":
            mark_task_complete(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            mark_task_incomplete(tasks)
        elif choice == "6":
            print("Goobdye")
            break
        else:
            print("Invalid choice. Try again.")
