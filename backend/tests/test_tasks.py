
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
    """Create a fresh Flask application for every test."""
    flask_app = task_app.create_app()
    flask_app.config["TESTING"] = True

    with flask_app.test_client() as test_client:
        yield test_client



def test_create_task(client):
    """A valid title should create a new task."""

    response = client.post(
        "/api/tasks",
        json={"title": "Practice pytest"},
    )

    assert response.status_code == 201
    assert response.get_json()["title"] == "Practice pytest"
    assert response.get_json()["is_complete"] is False
    assert response.get_json()["id"] == 3


def test_reject_blank_title(client):
    """A title containing only spaces should be rejected."""

    response = client.post(
        "/api/tasks",
        json={"title": "   "},
    )

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_missing_task(client):
    """A task that does not exist should return 404."""

    response = client.get("/api/tasks/999999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Task not found."


def test_reject_invalid_completion(client):
    """Completion must be a JSON boolean, not a string."""

    response = client.patch(
        "/api/tasks/1",
        json={"is_complete": "false"},
    )

    assert response.status_code == 400
    assert "boolean" in response.get_json()["error"]


def test_rejected_update_keeps_original_task(client):
    """An invalid PATCH must not change either stored field."""

    original = client.get("/api/tasks/1").get_json()

    response = client.patch(
        "/api/tasks/1",
        json={
            "title": "Changed",
            "is_complete": "false",
        },
    )

    assert response.status_code == 400

    unchanged = client.get("/api/tasks/1").get_json()

    assert unchanged["title"] == original["title"]
    assert unchanged["is_complete"] == original["is_complete"]
# Test                                  Expected result
# Creat a valid task                    HTTP 201
# Reject a blank title                  HTPP 400
# Request a missing task                HTTP 404
# Reject "false" as completion          HTTP 400
# Reject invalid mixef-filed PATCH      HTTP 400; original task unchanged