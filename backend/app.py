
"""Flask API for the Task Manager project."""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate

from config import get_database_url, get_frontend_origin
from models import db, Task
from validation import read_json_object, validate_title


def create_app(database_url=None):
    """Create a Flask application connected to PostgreSQL."""

    app = Flask(__name__)

    # Configure the PostgreSQL database connection.
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url or get_database_url()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Connect SQLAlchemy and Flask-Migrate.
    db.init_app(app)
    Migrate(app, db)

    # Allow requests from the React development server.
    CORS(
        app,
        resources={r"/api/*": {"origins": get_frontend_origin()}},
    )

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
        """Retrieve tasks from PostgreSQL."""
        status = request.args.get("status", "all")

        if status not in ("all", "active", "completed"):
            return jsonify({
                "error": "Status must be all, active, or completed."
            }), 400

        query = db.select(Task)

        if status == "active":
            query = query.where(Task.is_complete.is_(False))
        elif status == "completed":
            query = query.where(Task.is_complete.is_(True))

        query = query.order_by(Task.id.desc())

        tasks = db.session.execute(query).scalars().all()

        return jsonify([
            {
                "id": task.id,
                "title": task.title,
                "is_complete": task.is_complete,
                "created_at": task.created_at.isoformat(),
            }
            for task in tasks
        ])

    # READ: Get one task by its ID.
    @app.get("/api/tasks/<int:task_id>")
    def get_task(task_id):
        """Retrieve one task from PostgreSQL."""
        task = db.session.get(Task, task_id)

        if task is None:
            return jsonify({"error": "Task not found."}), 404

        return jsonify({
            "id": task.id,
            "title": task.title,
            "is_complete": task.is_complete,
            "created_at": task.created_at.isoformat(),
        })

    # CREATE: Save a new task in PostgreSQL.
    @app.post("/api/tasks")
    def create_task():
        """Create a new task and save it in PostgreSQL."""
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

        # Create a new SQLAlchemy task object.
        task = Task(title=title, is_complete=False)

        # Save the task permanently in PostgreSQL.
        db.session.add(task)
        db.session.commit()

        return jsonify({
            "id": task.id,
            "title": task.title,
            "is_complete": task.is_complete,
            "created_at": task.created_at.isoformat(),
        }), 201

    # UPDATE: Temporarily unavailable during Day 07.
    # PostgreSQL-backed editing will be implemented on Day 08.
    @app.patch("/api/tasks/<int:task_id>")
    def edit_task(task_id):
        return jsonify({
            "error": "Task editing is temporarily unavailable."
        }), 405

    # DELETE: Temporarily unavailable during Day 07.
    # PostgreSQL-backed deletion will be implemented on Day 08.
    @app.delete("/api/tasks/<int:task_id>")
    def remove_task(task_id):
        return jsonify({
            "error": "Task deletion is temporarily unavailable."
        }), 405

    # Return a JSON error for an unknown route.
    @app.errorhandler(404)
    def route_not_found(error):
        return jsonify({
            "error": "Route not found."
        }), 404

    # Return a JSON error for an unsupported HTTP method.
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "HTTP method not allowed for this route."
        }), 405

    # Information about the backend.
    @app.get("/api/about")
    def about():
        return jsonify({
            "language": "Python",
            "framework": "Flask",
            "storage": "PostgreSQL",
        })

    # Return the configured Flask application.
    return app


# Keep the existing Flask startup command working.
app = create_app()
