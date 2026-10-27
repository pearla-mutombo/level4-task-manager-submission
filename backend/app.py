
"""Flask API for the Task Manager project."""

from datetime import datetime, timezone

from flask import Flask, current_app, jsonify, request
from flask_cors import CORS

from config import get_frontend_origin
from storage import create_initial_tasks, find_task
from validation import read_json_object, validate_title


def create_app():
    """Create a Flask application with a fresh in-memory task store."""

    app = Flask(__name__)

    # Allow requests from the React development server.
    CORS(
        app,
        resources={r"/api/*": {"origins": get_frontend_origin()}},
    )

    # Give each new Flask application its own task list.
    app.task_store = create_initial_tasks()

    # Start new task IDs after the two sample tasks.
    app.next_task_id = 3

    # Check whether the Flask backend is running.
    @app.get("/api/health")
    def health():
        return jsonify({
            "status": "ok",
            "message": "Hello from Flask",
        })

    # Instructor's example endpoint.
    @app.get("/api/me")
    def me():
        return jsonify({
            "name": "Ulises",
            "favorite_color": "green",
        })

    # READ: Get all tasks or filter by completion status.
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

        # Show the newest tasks first.
        matching_tasks.sort(
            key=lambda task: task["id"],
            reverse=True,
        )

        return jsonify(matching_tasks)

    # READ: Get one task by its ID.
    @app.get("/api/tasks/<int:task_id>")
    def get_task(task_id):
        task = find_task(current_app.task_store, task_id)

        if task is None:
            return jsonify({"error": "Task not found."}), 404

        return jsonify(task)

    # CREATE: Add a new task.
    @app.post("/api/tasks")
    def create_task():
        data, error, status = read_json_object()

        if error is not None:
            return jsonify({"error": error}), status

        # Only the title is allowed when creating a task.
        if set(data) - {"title"}:
            return jsonify({
                "error": "Only title is allowed when creating a task."
            }), 400

        title, error = validate_title(data.get("title"))

        if error is not None:
            return jsonify({"error": error}), 400

        # The backend creates the ID and timestamp.
        task = {
            "id": current_app.next_task_id,
            "title": title,
            "is_complete": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        current_app.task_store.append(task)
        current_app.next_task_id += 1

        return jsonify(task), 201

    # UPDATE: Change a task's title or completion status.
    @app.patch("/api/tasks/<int:task_id>")
    def edit_task(task_id):
        task = find_task(current_app.task_store, task_id)

        if task is None:
            return jsonify({"error": "Task not found."}), 404

        data, error, status = read_json_object()

        if error is not None:
            return jsonify({"error": error}), status

        if not data:
            return jsonify({
                "error": "Provide title and/or is_complete."
            }), 400

        # Prevent changes to protected fields.
        if set(data) - {"title", "is_complete"}:
            return jsonify({
                "error": "Only title and is_complete can be updated."
            }), 400

        # Validate everything before changing the task.
        # This prevents partially saving an invalid update.
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

        # Apply changes only after all validation passes.
        task.update(changes)

        return jsonify(task)

    # DELETE: Remove one task.
    @app.delete("/api/tasks/<int:task_id>")
    def remove_task(task_id):
        task = find_task(current_app.task_store, task_id)

        if task is None:
            return jsonify({"error": "Task not found."}), 404

        current_app.task_store.remove(task)

        # HTTP 204 means success with no response body.
        return "", 204

    # Return a JSON error for an unknown route.
    @app.errorhandler(404)
    def route_not_found(error):
        return jsonify({"error": "Route not found."}), 404

    # Return a JSON error for an unsupported HTTP method.
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "HTTP method not allowed for this route."
        }), 405

    # Day 1 endpoint: Information about the backend.
    @app.get("/api/about")
    def about():
        return jsonify({
            "language": "Python",
            "framework": "Flask",
            "storage": "in-memory",
        })

    # Return the configured Flask application.
    return app


# Keep the existing Flask startup command working.
app = create_app()
