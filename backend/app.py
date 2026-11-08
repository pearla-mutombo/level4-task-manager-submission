
"""Flask API for the Task Manager project."""

from flask import Flask, jsonify, request, g
from flask_cors import CORS
from flask_migrate import Migrate

from config import get_database_url, get_frontend_origin
from auth import get_access_token, verify_access_token
from models import db, Task, Category
from validation import read_json_object, validate_title

def create_app(database_url=None):
    """Create a Flask application connected to PostgreSQL."""

    app = Flask(__name__)

    # Configure the PostgreSQL database connection.
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url or get_database_url()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Keep database connections small and reliable for Render Free.
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_size": 2,
        "max_overflow": 0,
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # Connect SQLAlchemy and Flask-Migrate.
    db.init_app(app)
    Migrate(app, db)
    
    # Allow requests from the React development server.
    CORS(
        app,
        resources={r"/api/*": {"origins": get_frontend_origin()}},
    )

    # Business endpoints require a verified Supabase user.
    PROTECTED_ENDPOINTS = {
        "get_tasks",
        "get_task",
        "get_categories",
        "create_category",
        "update_category",
        "delete_category",
        "create_task",
        "edit_task",
        "remove_task",
    }

    @app.before_request
    def require_authentication():
        """Verify the user before accessing protected endpoints."""

        # Allow browser CORS preflight requests without authentication.
        if request.method == "OPTIONS":
            return None

        if request.endpoint not in PROTECTED_ENDPOINTS:
            return None

        token = get_access_token()

        if not token:
            return jsonify({"error": "Authentication required"}), 401

        try:
            user = verify_access_token(token)
        except ConnectionError:
            return jsonify({"error": "Authentication service unavailable"}), 503

        if user is None:
            return jsonify({"error": "Invalid or expired token"}), 401

        g.current_user_id = user.id
        return None

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

    # READ: Get all tasks or filter by status and category.
    @app.get("/api/tasks")
    def get_tasks():
        """Retrieve tasks from PostgreSQL with optional filters."""
        status = request.args.get("status", "all")
        category_id = request.args.get("category_id")

        # Validate the completion-status filter.
        if status not in ("all", "active", "completed"):
            return jsonify({
                "error": "Status must be all, active, or completed."
            }), 400

        query = db.select(Task).where(Task.user_id == g.current_user_id)
        # Task.user_id identifies the task's owner.
        # g.current_user_id contains the user ID obtained from the verified Supabase
        # access token.
        # .where(...) limits the result to tasks belonging to that authenticated user.

        # Filter tasks by completion status.
        if status == "active":
            query = query.where(Task.is_complete.is_(False))
        elif status == "completed":
            query = query.where(Task.is_complete.is_(True))

        # Filter tasks by category when a category ID is provided.
        if category_id is not None:
            try:
                category_id = int(category_id)
            except ValueError:
                return jsonify({
                    "error": "category_id must be an integer."
                }), 400

            if category_id <= 0:
                return jsonify({
                    "error": "category_id must be a positive integer."
                }), 400

            query = query.where(Task.category_id == category_id)

        # Return the newest tasks first.
        tasks = db.session.execute(query).scalars().all()

        return jsonify([
            {
                "id": task.id,
                "title": task.title,
                "category_id": task.category_id,
                "is_complete": task.is_complete,
                "created_at": task.created_at.isoformat(),
            }
            for task in tasks
        ])

    # READ: Get one task by its ID.
    @app.get("/api/tasks/<int:task_id>")
    def get_task(task_id):
        """Retrieve one task from PostgreSQL."""
        task = db.session.execute(
            db.select(Task).where(
                Task.id == task_id,
                Task.user_id == g.current_user_id,
            )
        ).scalar_one_or_none()
# Task.id == task_id finds the requested task.
# Task.user_id == g.current_user_id checks that the authenticated user owns it.
# .scalar_one_or_none() returns the matching tasks or None.

        if task is None:
            return jsonify({"error": "Task not found."}), 404

        return jsonify({
            "id": task.id,
            "title": task.title,
            "category_id": task.category_id,
            "is_complete": task.is_complete,
            "created_at": task.created_at.isoformat(),
        })

    # READ: Get all categories in alphabetical order.
    @app.get("/api/categories")
    def get_categories():
        """Return all categories from PostgreSQL."""
        query = (
            db.select(Category)
            .where(Category.user_id == g.current_user_id)
            .order_by(Category.name.asc())
        )
# Caterofy.user_id identifies the category's owner
# g.current_user_id contains the authenticated user's verified Supabase ID.
# .where(...) limits the results to the categories belonging to that user.
# .order_by(...) keeps the categories sorted alphabetically.
        categories = db.session.execute(query).scalars().all()

        return jsonify([
            {
                "id": category.id,
                "name": category.name,
            }
            for category in categories
        ])

    # CREATE: Save a new category in PostgreSQL.
    @app.post("/api/categories")
    def create_category():
        """Create a new category in PostgreSQL."""
        data, error, status = read_json_object()

        if error is not None:
            return jsonify({"error": error}), status

        if set(data) - {"name"}:
            return jsonify({"error": "Only name is allowed."}), 400

        name = data.get("name")

        if not isinstance(name, str) or not name.strip():
            return jsonify({"error": "Category name is required."}), 400

        name = name.strip()

        if len(name) > 40:
            return jsonify({
                "error": "Category name must be 40 characters or fewer."
            }), 400

        existing = db.session.execute(
            db.select(Category).where(
                Category.name == name,
                Category.user_id == g.current_user_id,
            )
        ).scalar_one_or_none()

        if existing is not None:
            return jsonify({"error": "Category already exists."}), 409

        category = Category(
            name=name,
            user_id=g.current_user_id,
        )
        db.session.add(category)
        db.session.commit()

        return jsonify({
            "id": category.id,
            "name": category.name,
        }), 201

    # UPDATE: Rename an existing category in PostgreSQL.
    @app.patch("/api/categories/<int:category_id>")
    def update_category(category_id):
        """Update a category name in PostgreSQL."""
        category = db.session.execute(
            db.select(Category).where(
                Category.id == category_id,
                Category.user_id == g.current_user_id,
            )
        ).scalar_one_or_none()

        if category is None:
            return jsonify({"error": "Category not found."}), 404

        data, error, status = read_json_object()

        if error is not None:
            return jsonify({"error": error}), status

        if set(data) != {"name"}:
            return jsonify({"error": "Only name is required."}), 400

        name = data.get("name")

        if not isinstance(name, str) or not name.strip():
            return jsonify({"error": "Category name is required."}), 400

        name = name.strip()

        if len(name) > 40:
            return jsonify({
                "error": "Category name must be 40 characters or fewer."
            }), 400

        existing = db.session.execute(
            db.select(Category).where(
                Category.name == name,
                Category.user_id == g.current_user_id,
                Category.id != category_id,
            )
        ).scalar_one_or_none()

        if existing is not None:
            return jsonify({"error": "Category already exists."}), 409

        category.name = name
        db.session.commit()

        return jsonify({
            "id": category.id,
            "name": category.name,
        })

    # DELETE: Remove a category without deleting its tasks.
    @app.delete("/api/categories/<int:category_id>")
    def delete_category(category_id):
        """Delete a category from PostgreSQL."""
        category = db.session.execute(
            db.select(Category).where(
                Category.id == category_id,
                Category.user_id == g.current_user_id,
            )
        ).scalar_one_or_none()
        # Category.id == category.id identifies the requested category.
        # Category.user_id == g.current_user_id checks that the category belongs
        # to the authenticated user.
        # .scalar_one_or_none() return the category only when both conditions
        # match.

        if category is None:
            return jsonify({"error": "Category not found."}), 404

        db.session.delete(category)
        db.session.commit()

        return "", 204

    # CREATE: Save a new task with an optional category.
    @app.post("/api/tasks")
    def create_task():
        """Create a task in PostgreSQL, optionally assigning a category."""
        data, error, status = read_json_object()

        if error is not None:
            return jsonify({"error": error}), status

        if set(data) - {"title", "category_id"}:
            return jsonify({
                "error": "Only title and category_id are allowed."
            }), 400

        title, error = validate_title(data.get("title"))

        if error is not None:
            return jsonify({"error": error}), 400

        category_id = data.get("category_id")

        if category_id is not None:
            if type(category_id) is not int:
                return jsonify({
                    "error": "category_id must be an integer or null."
                }), 400

            category = db.session.execute(
                db.select(Category).where(
                    Category.id == category_id,
                    Category.user_id == g.current_user_id,
                )
            ).scalar_one_or_none()
            # Category.id == category_id checks the requested category.
            # Category.user_id == g.current_user_id verifies that the category belonhs
            # to the authenticated user.
            # .scalar_one_or_none() returns the catefory only when both conditions match.

            if category is None:
                return jsonify({
                    "error": "Category not found."
                }), 404

        task = Task(
            title=title,
            category_id=category_id,
            is_complete=False,
            user_id=g.current_user_id,
        )

        db.session.add(task)
        db.session.commit()

        return jsonify({
            "id": task.id,
            "title": task.title,
            "category_id": task.category_id,
            "is_complete": task.is_complete,
            "created_at": task.created_at.isoformat(),
        }), 201

     # UPDATE: Edit an existing task in PostgreSQL.
    @app.patch("/api/tasks/<int:task_id>")
    def edit_task(task_id):
        """Update a task's title, completion status, or category."""
        task = db.session.execute(
            db.select(Task).where(
                Task.id == task_id,
                Task.user_id == g.current_user_id,
            )
        ).scalar_one_or_none()
        # Task.id == task_id identifies the task being edited.
        # Task.user_id == g.current_user_id ensures the task belongs to the
        # authenticated Supabase user.
        # .scalar_one_or_noe() returns the task only when both conditions match.

        if task is None:
            return jsonify({"error": "Task not found."}), 404

        data, error, status = read_json_object()

        if error is not None:
            return jsonify({"error": error}), status

        allowed_fields = {"title", "is_complete", "category_id"}

        if not data or set(data) - allowed_fields:
            return jsonify({
                "error": "Provide title, is_complete, or category_id only."
            }), 400

        # Validate the title before making any changes.
        if "title" in data:
            title, error = validate_title(data["title"])

            if error is not None:
                return jsonify({"error": error}), 400

        # Validate the completion status.
        if "is_complete" in data:
            if not isinstance(data["is_complete"], bool):
                return jsonify({
                    "error": "is_complete must be true or false."
                }), 400

        # Validate the category if one was provided.
        if "category_id" in data:
            category_id = data["category_id"]

            if category_id is not None:
                if type(category_id) is not int:
                    return jsonify({
                        "error": "category_id must be an integer or null."
                    }), 400

                category = db.session.execute(
                    db.select(Category).where(
                        Category.id == category_id,
                        Category.user_id == g.current_user_id,
                    )
                ).scalar_one_or_none()
                # Category.id == category_id identifies the requested category.
                # Category.user_id == g.current_user_id verifies that the category belongs
                # to the authenticated user.
                # .scalar_one_or_none() returns the category only when both conditions match.

                if category is None:
                    return jsonify({
                        "error": "Category not found."
                    }), 404

        # Apply the validated changes.
        if "title" in data:
            task.title = title

        if "is_complete" in data:
            task.is_complete = data["is_complete"]

        if "category_id" in data:
            task.category_id = data["category_id"]

        db.session.commit()

        return jsonify({
            "id": task.id,
            "title": task.title,
            "category_id": task.category_id,
            "is_complete": task.is_complete,
            "created_at": task.created_at.isoformat(),
        })

    # DELETE: Remove an existing task from PostgreSQL.
    @app.delete("/api/tasks/<int:task_id>")
    def remove_task(task_id):
        """Delete a task permanently from PostgreSQL."""
        task = db.session.execute(
            db.select(Task).where(
                Task.id == task_id,
                Task.user_id == g.current_user_id,
            )
        ).scalar_one_or_none()
        # Task.id == task_id identifies the task being deleted.
        # Task.user_id == g.current_user_id verifies that the authenticated user
        # owns the task.
        # .scalar_one_or_none() returns the task only when both conditions match.

        if task is None:
            return jsonify({"error": "Task not found."}), 404

        db.session.delete(task)
        db.session.commit()

        return "", 204

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
