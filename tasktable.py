import json
import os
from uuid import uuid4

from bottle import Bottle, redirect, request, static_file, template


def load_tasks(db_path):
    with open(db_path, "r", encoding="utf-8") as tasks_file:
        payload = json.load(tasks_file)
    tasks = payload.get("tasks", [])
    updated = False
    for task in tasks:
        if not task.get("id"):
            task["id"] = str(uuid4())
            updated = True
    if updated:
        save_tasks(db_path, tasks)
    return tasks


def save_tasks(db_path, tasks):
    with open(db_path, "w", encoding="utf-8") as tasks_file:
        json.dump({"tasks": tasks}, tasks_file, indent=4, ensure_ascii=False)


def create_app(db_path=None):
    app = Bottle()
    resolved_db_path = db_path or os.environ.get("TASKTABLE_DB_PATH", "database.json")

    @app.get("/")
    def index():
        tasks = load_tasks(resolved_db_path)
        return template("templates/tasktable.tpl", tasks=tasks)

    @app.post("/tasks/add")
    def add_task():
        tasks = load_tasks(resolved_db_path)
        task = {
            "id": str(uuid4()),
            "project": request.forms.get("project", "").strip(),
            "title": request.forms.get("title", "").strip(),
            "status": request.forms.get("status", "").strip(),
            "priority": request.forms.get("priority", "").strip(),
        }
        tasks.append(task)
        save_tasks(resolved_db_path, tasks)
        return redirect("/")

    @app.post("/tasks/<task_id>/update")
    def update_task(task_id):
        tasks = load_tasks(resolved_db_path)
        for task in tasks:
            if task.get("id") == task_id:
                task["project"] = request.forms.get("project", task.get("project", "")).strip()
                task["title"] = request.forms.get("title", task.get("title", "")).strip()
                task["status"] = request.forms.get("status", task.get("status", "")).strip()
                task["priority"] = request.forms.get("priority", task.get("priority", "")).strip()
                save_tasks(resolved_db_path, tasks)
                break
        return redirect("/")

    @app.post("/tasks/<task_id>/delete")
    def delete_task(task_id):
        tasks = load_tasks(resolved_db_path)
        tasks = [task for task in tasks if task.get("id") != task_id]
        save_tasks(resolved_db_path, tasks)
        return redirect("/")

    @app.route("/static/<filepath:path>")
    def serve_static(filepath):
        return static_file(filepath, root="./static")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, reloader=True)
