# Build this file together in Day 1.
# 1. Import Flask and jsonify.
# 2. Import CORS from flask_cors.
# 3. Create a Flask application named app.
# 4. Allow the supplied frontend origin for /api routes.
# 5. Define GET /api/health to return a JSON greeting.
# This starter intentionally cannot serve requests until those steps are complete.

# First we import Flask
from flask import Flask, jsonify, request

# Import new CORS library
from flask_cors import CORS

from datetime import datetime, timezone

from werkzeug.exceptions import BadRequest

# Create a Flask application
app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5173"}})

# Simulate a database in memory
tasks = [
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
next_id = 3

def find_task(task_id):
  for task in tasks:
    if task["id"] == task_id:
      return task
  return None

def read_json_object():
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
    if not isinstance(value, str):
        return None, "Title must be a string."
    title = value.strip()
    if not 1 <= len(title) <= 80:
        return None, "Title must contain between 1 and 80 characters."
    return title, None

# Define endpoint name and below its functionality
@app.get("/api/health")
def health():
  return jsonify({"status": "ok", "message": "Hello from Flask"})

# Testing endpoint
@app.get("/api/me")
def me():
  return jsonify({"name": "Ulises", "favorite_color": "green"})

# RestFull API definitions
# GET - retrieve data from the server
# POST - send data to the server
# PUT - update existing data on the server
# PATCH - partially update existing data on the server
# DELETE - remove data from the server

# GET /tasks request
# This endpoint would return to the user all the tasks available
@app.get("/api/tasks")
def get_tasks():
    status = request.args.get("status", "all")
    if status not in ("all", "active", "completed"):
        return jsonify({"error": "Status must be all, active, or completed."}), 400

    matching_tasks = []
    for task in tasks:
        if status == "all":
            matching_tasks.append(task)
        elif status == "active" and not task["is_complete"]:
            matching_tasks.append(task)
        elif status == "completed" and task["is_complete"]:
            matching_tasks.append(task)

    # IDs increase on creation, so the highest ID is the newest task.
    matching_tasks.sort(key=lambda task: task["id"], reverse=True)
    return jsonify(matching_tasks)

# GET /task/:id
# This endpoint will return a single task
@app.get("/api/tasks/<int:task_id>")
def get_task(task_id):
    task = find_task(task_id)
    if task is None:
        return jsonify({"error": "Task not found."}), 404
    return jsonify(task)

# POST /tasks
# This endpoint will create a new task
@app.post("/api/tasks")
def create_task():
  global next_id

  data, error, status = read_json_object()
  if error is not None:
      return jsonify({"error": error}), status

  if set(data) - {"title"}:
      return jsonify({"error": "Only title is allowed when creating a task."}), 400

  title, error = validate_title(data.get("title"))
  if error is not None:
      return jsonify({"error": error}), 400

  task = {
    "id": next_id,
    "title": title,
    "is_complete": False,
    "created_at": datetime.now(timezone.utc).isoformat(),
  }

  tasks.append(task)
  next_id += 1
  return jsonify(task), 201

# PATCH /tasks/:id
# This endpoint will partially update an existing task
@app.patch("/api/tasks/<int:task_id>")
def edit_task(task_id):
  task = find_task(task_id)
  if task is None:
    return jsonify({"error": "Task not found."}), 404

  data, error, status = read_json_object()
  if error is not None:
    return jsonify({"error": error}), status

  if not data:
    return jsonify({"error": "Provide title and/or is_complete."}), 400
  if set(data) - {"title", "is_complete"}:
    return jsonify({"error": "Only title and is_complete can be updated."}), 400

  changes = {}
  if "title" in data:
    title, error = validate_title(data["title"])
    if error is not None:
        return jsonify({"error": error}), 400
    changes["title"] = title

  if "is_complete" in data:
      if not isinstance(data["is_complete"], bool):
          return jsonify({"error": "is_complete must be a boolean."}), 400
      changes["is_complete"] = data["is_complete"]

  # No stored value changes until every supplied field has passed validation.
  task.update(changes)
  return jsonify(task)

@app.delete("/api/tasks/<int:task_id>")
def remove_task(task_id):
  task = find_task(task_id)
  if task is None:
      return jsonify({"error": "Task not found."}), 404
  tasks.remove(task)
  return "", 204

@app.errorhandler(404)
def route_not_found(error):
    return jsonify({"error": "Route not found."}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "HTTP method not allowed for this route."}), 405

# Day 1 Exercise: Return information about our backend
@app.get("/api/about")
def about():
    return jsonify({
        "language": "Python",
        "framework": "Flask",
        "storage": "In-memory"
    })
