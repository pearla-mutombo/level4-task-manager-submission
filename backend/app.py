
"""Flask API for the Task Manager project."""

from datetime import datetime, timezone

from flask import Flask, current_app, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import BadRequest

from config import get_frontend_origin


def create_app():
    """Create a Flask application with a fresh in-memory task store."""
    app = Flask(__name__)

    # Allow requests from the React development server.
    CORS(
        app,
        resources={r"/api/*": {"origins": get_frontend_origin()}},
    )

    # Every new Flask application gets its own starting data.
    app.task_store = [
        {
            "id": 1,
            "title": "Trace a request from React to Flask",
            "is_complete": False,
            "created_at": "2026-10-12T12:00:00Z",
        },
        {
            "id": 2,
            "title": "Practice Python lists and dictionaries",
            "is_complete": True,
            "created_at": "2026-10-12T12:05:00Z",
        },
    ]
    app.next_task_id = 3

    @app.get("/api/health")
    def health():
        return jsonify({
            "status": "ok",
            "message": "Hello from Flask",
        })

    @app.get("/api/me")
    def me():
        return jsonify({
            "name": "Ulises",
            "favorite_color": "green",
        })

    @app.get("/api/tasks")
    def get_tasks():
        status = request.args.get("status", "all")

        if status not in ("all", "active", "completed"):
            return jsonify({
                "error": "Status must be all, active, or completed."
            }), 400

        tasks = current_app.task_store

        if status == "active":
            matching_tasks = [
                task for task in tasks if not task["is_complete"]
            ]
        elif status == "completed":
            matching_tasks = [
                task for task in tasks if task["is_complete"]
            ]
        else:
            matching_tasks = list(tasks)

        matching_tasks.sort(
            key=lambda task: task["id"],
            reverse=True,
        )
        return jsonify(matching_tasks)

    @app.get("/api/tasks/<int:task_id>")
    def get_task(task_id):
        task = find_task(task_id)

        if task is None:
            return jsonify({"error": "Task not found."}), 404

        return jsonify(task)

    @app.post("/api/tasks")
    def create_task():
        data, error, status = read_json_object()

        if error is not None:
            return jsonify({"error": error}), status

        if set(data) - {"title"}:
            return jsonify({
                "error": "Only title is allowed when creating a task."
            }), 400

        title, error = validate_title(data.get("title"))

        if error is not None:
            return jsonify({"error": error}), 400

        task = {
            "id": current_app.next_task_id,
            "title": title,
            "is_complete": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        current_app.task_store.append(task)
        current_app.next_task_id += 1

        return jsonify(task), 201

    @app.patch("/api/tasks/<int:task_id>")
    def edit_task(task_id):
        task = find_task(task_id)

        if task is None:
            return jsonify({"error": "Task not found."}), 404

        data, error, status = read_json_object()

        if error is not None:
            return jsonify({"error": error}), status

        if not data:
            return jsonify({
                "error": "Provide title and/or is_complete."
            }), 400

        if set(data) - {"title", "is_complete"}:
            return jsonify({
                "error": "Only title and is_complete can be updated."
            }), 400

        # Validate everything before changing the stored task.
        changes = {}

        if "title" in data:
            title, error = validate_title(data["title"])

            if error is not None:
                return jsonify({"error": error}), 400

            changes["title"] = title

        if "is_complete" in data:
            if not isinstance(data["is_complete"], bool):
                return jsonify({
                    "error": "is_complete must be a boolean."
                }), 400

            changes["is_complete"] = data["is_complete"]

        task.update(changes)
        return jsonify(task)

    @app.delete("/api/tasks/<int:task_id>")
    def remove_task(task_id):
        task = find_task(task_id)

        if task is None:
            return jsonify({"error": "Task not found."}), 404

        current_app.task_store.remove(task)
        return "", 204

    @app.errorhandler(404)
    def route_not_found(error):
        return jsonify({"error": "Route not found."}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "HTTP method not allowed for this route."
        }), 405

    # Day 1 endpoint: information about the backend.
    @app.get("/api/about")
    def about():
        return jsonify({
            "language": "Python",
            "framework": "Flask",
            "storage": "in-memory",
        })

    # Return the configured Flask application.
    return app


def find_task(task_id):
    """Find one task in the current application's store."""
    for task in current_app.task_store:
        if task["id"] == task_id:
            return task

    return None


def read_json_object():
    """Read a request body and verify it contains a JSON object."""
    if not request.is_json:
        return None, "Send the request body as application/json.", 415

    try:
        data = request.get_json()
    except BadRequest:
        return None, "Request body must be valid JSON.", 400

    if not isinstance(data, dict):
        return None, "Request body must be a JSON object.", 400

    return data, None, None


def validate_title(value):
    """Require a title containing 1 to 80 characters."""
    if not isinstance(value, str):
        return None, "Title must be a string."

    title = value.strip()

    if not 1 <= len(title) <= 80:
        return None, "Title must contain between 1 and 80 characters."

    return title, None
# Keep the existing Flask startup command working.
app = create_app()