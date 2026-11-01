
"""Day 4: Automated tests for the Flask Task Manager API."""

import sys
from pathlib import Path

import pytest

# Allow Python to find app.py in the backend folder.
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

import app as task_app



@pytest.fixture
def client():
    """Use the separate PostgreSQL testing database."""

    from config import get_test_database_url
    from models import db, Task

    # Never run these tests against the development database.
    test_database_url = get_test_database_url()

    assert test_database_url is not None, (
        "TEST_DATABASE_URL must be configured."
    )

    assert test_database_url != task_app.get_database_url(), (
        "The testing and development databases must be different."
    )

    flask_app = task_app.create_app(
        database_url=test_database_url
    )
    flask_app.config["TESTING"] = True

    with flask_app.app_context():
        # Clear only the testing database before each test.
        db.session.execute(db.delete(Task))
        db.session.commit()

    with flask_app.test_client() as test_client:
        yield test_client

    with flask_app.app_context():
        db.session.remove()





def test_create_task(client):
    """A valid title should create a task in PostgreSQL."""

    response = client.post(
        "/api/tasks",
        json={"title": "Practice pytest"},
    )

    assert response.status_code == 201

    task = response.get_json()

    assert task["title"] == "Practice pytest"
    assert task["is_complete"] is False
    assert isinstance(task["id"], int)
    assert task["id"] > 0
    assert "created_at" in task

    # Confirm the task can be retrieved from PostgreSQL.
    saved_response = client.get(f"/api/tasks/{task['id']}")

    assert saved_response.status_code == 200
    assert saved_response.get_json()["title"] == "Practice pytest"



def test_editing_temporarily_disabled(client):
    """Task editing should be unavailable during Day 07."""

    response = client.patch(
        "/api/tasks/1",
        json={"is_complete": "false"},
    )

    assert response.status_code == 405
    assert response.get_json()["error"] == (
        "Task editing is temporarily unavailable."
    )


def test_missing_task(client):
    """A task that does not exist should return 404."""

    response = client.get("/api/tasks/999999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Task not found."


def test_editing_temporarily_disabled(client):
    """Task editing should be unavailable during Day 07."""

    response = client.patch(
        "/api/tasks/1",
        json={"is_complete": "false"},
    )

    assert response.status_code == 405
    assert response.get_json()["error"] == (
        "Task editing is temporarily unavailable."
    )


def test_deleting_temporarily_disabled(client):
    """Task deletion should be unavailable during Day 07."""

    response = client.delete("/api/tasks/1")

    assert response.status_code == 405
    assert response.get_json()["error"] == (
        "Task deletion is temporarily unavailable."
    )

def test_reject_blank_title(client):
    """A title containing only spaces should be rejected."""

    response = client.post(
        "/api/tasks",
        json={"title": "   "},
    )

    assert response.status_code == 400
    assert "error" in response.get_json()
# Test                                  Expected result
# Creat a valid task                    HTTP 201
# Reject a blank title                  HTPP 400
# Request a missing task                HTTP 404
# Reject "false" as completion          HTTP 400
# Reject invalid mixef-filed PATCH      HTTP 400; original task unchanged