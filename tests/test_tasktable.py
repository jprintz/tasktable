import io
import json
import os
import sys
from urllib.parse import urlencode
from wsgiref.util import setup_testing_defaults

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tasktable


def call_app(app, method, path, data=None):
    environ = {}
    setup_testing_defaults(environ)
    environ["REQUEST_METHOD"] = method
    environ["PATH_INFO"] = path
    body = b""
    if data:
        body = urlencode(data).encode()
        environ["CONTENT_TYPE"] = "application/x-www-form-urlencoded"
    environ["CONTENT_LENGTH"] = str(len(body))
    environ["wsgi.input"] = io.BytesIO(body)
    response_status = {}
    response_headers = {}

    def start_response(status, headers):
        response_status["status"] = status
        response_headers.update(dict(headers))

    payload = b"".join(app(environ, start_response))
    return response_status["status"], response_headers, payload


def write_db(path, tasks):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump({"tasks": tasks}, handle, indent=4, ensure_ascii=False)


def read_db(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)["tasks"]


def test_add_task(tmp_path):
    db_path = tmp_path / "db.json"
    write_db(db_path, [])
    app = tasktable.create_app(str(db_path))

    status, _, _ = call_app(
        app,
        "POST",
        "/tasks/add",
        {
            "project": "Alpha",
            "title": "Plan",
            "status": "New",
            "priority": "2",
        },
    )

    assert status.startswith(("302", "303"))
    tasks = read_db(db_path)
    assert len(tasks) == 1
    assert tasks[0]["project"] == "Alpha"
    assert tasks[0]["title"] == "Plan"
    assert tasks[0]["status"] == "New"
    assert tasks[0]["priority"] == "2"
    assert tasks[0]["id"]


def test_update_task(tmp_path):
    db_path = tmp_path / "db.json"
    write_db(
        db_path,
        [
            {
                "id": "task-1",
                "project": "Alpha",
                "title": "Plan",
                "status": "New",
                "priority": "2",
            }
        ],
    )
    app = tasktable.create_app(str(db_path))

    status, _, _ = call_app(
        app,
        "POST",
        "/tasks/task-1/update",
        {
            "project": "Beta",
            "title": "Execute",
            "status": "In Progress",
            "priority": "1",
        },
    )

    assert status.startswith(("302", "303"))
    tasks = read_db(db_path)
    assert tasks[0]["project"] == "Beta"
    assert tasks[0]["title"] == "Execute"
    assert tasks[0]["status"] == "In Progress"
    assert tasks[0]["priority"] == "1"


def test_delete_task(tmp_path):
    db_path = tmp_path / "db.json"
    write_db(
        db_path,
        [
            {
                "id": "task-1",
                "project": "Alpha",
                "title": "Plan",
                "status": "New",
                "priority": "2",
            },
            {
                "id": "task-2",
                "project": "Beta",
                "title": "Execute",
                "status": "In Progress",
                "priority": "1",
            },
        ],
    )
    app = tasktable.create_app(str(db_path))

    status, _, _ = call_app(app, "POST", "/tasks/task-1/delete")

    assert status.startswith(("302", "303"))
    tasks = read_db(db_path)
    assert [task["id"] for task in tasks] == ["task-2"]
