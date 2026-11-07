
"""Automated tests for the Flask Task Manager API."""

import sys
from pathlib import Path
from types import SimpleNamespace
from uuid import UUID

import pytest

# Allow Python to find app.py in the backend folder.
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

import app as task_app
TEST_USER_ID = UUID("11111111-1111-4111-8111-111111111111")
SECOND_USER_ID = UUID("22222222-2222-4222-8222-222222222222")


@pytest.fixture
def client(monkeypatch):
    """Use only the isolated PostgreSQL test database and mock Supabase."""
    from config import get_test_database_url
    from models import db, Task, Category

    test_database_url = get_test_database_url()
    assert test_database_url, "TEST_DATABASE_URL must be configured."
    assert test_database_url != task_app.get_database_url(), (
        "Testing and development databases must be different."
    )

    flask_app = task_app.create_app(database_url=test_database_url)
    flask_app.config["TESTING"] = True
    monkeypatch.setattr(
        task_app,
        "verify_access_token",
        lambda token: SimpleNamespace(id=TEST_USER_ID),
    )

    with flask_app.app_context():
        # These deletes are intentionally limited to the dedicated test database.
        db.session.execute(db.delete(Task))
        db.session.execute(db.delete(Category))
        db.session.commit()

    with flask_app.test_client() as test_client:
        test_client.environ_base["HTTP_AUTHORIZATION"] = "Bearer test-token"
        yield test_client

    with flask_app.app_context():
        db.session.remove()


def act_as(monkeypatch, user_id):
    """Simulate a verified Supabase identity for a single test."""
    monkeypatch.setattr(
        task_app,
        "verify_access_token",
        lambda token: SimpleNamespace(id=user_id),
    )



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

def test_missing_task(client):
    """A task that does not exist should return 404."""

    response = client.get("/api/tasks/999999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Task not found."

def test_edit_task(client):
    """An existing task can be updated in PostgreSQL."""

    # Create a task specifically for this test.
    create_response = client.post(
        "/api/tasks",
        json={"title": "Original task title"},
    )

    assert create_response.status_code == 201

    task_id = create_response.get_json()["id"]

    # Update the task's title and completion status.
    response = client.patch(
        f"/api/tasks/{task_id}",
        json={
            "title": "Updated task title",
            "is_complete": True,
        },
    )

    assert response.status_code == 200

    updated_task = response.get_json()

    assert updated_task["title"] == "Updated task title"
    assert updated_task["is_complete"] is True

    # Confirm the changes were saved in PostgreSQL.
    get_response = client.get(f"/api/tasks/{task_id}")

    assert get_response.status_code == 200
    assert get_response.get_json()["title"] == "Updated task title"
    assert get_response.get_json()["is_complete"] is True

def test_delete_task(client):
    """An existing task can be deleted from PostgreSQL."""

    # Create a task specifically for this test.
    create_response = client.post(
        "/api/tasks",
        json={"title": "Task to delete"},
    )

    assert create_response.status_code == 201

    task_id = create_response.get_json()["id"]

    # Delete the newly created task.
    delete_response = client.delete(
        f"/api/tasks/{task_id}"
    )

    assert delete_response.status_code == 204

    # Confirm the task no longer exists.
    get_response = client.get(
        f"/api/tasks/{task_id}"
    )

    assert get_response.status_code == 404
    assert get_response.get_json() == {
        "error": "Task not found."
    }

def test_reject_blank_title(client):
    """A title containing only spaces should be rejected."""

    response = client.post(
        "/api/tasks",
        json={"title": "   "},
    )

    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_category(client):
    """A category can be created and retrieved from PostgreSQL."""

    # Create a new category.
    response = client.post(
        "/api/categories",
        json={"name": "Work"},
    )

    assert response.status_code == 201

    category = response.get_json()

    assert category["name"] == "Work"
    assert isinstance(category["id"], int)
    assert category["id"] > 0

    # Confirm the category appears in the saved category list.
    list_response = client.get("/api/categories")

    assert list_response.status_code == 200

    categories = list_response.get_json()

    assert any(
        item["id"] == category["id"] and item["name"] == "Work"
        for item in categories
    )

def test_update_category(client):
    """An existing category can be renamed in PostgreSQL."""

    # Create a category for this test.
    create_response = client.post(
        "/api/categories",
        json={"name": "Personal"},
    )

    assert create_response.status_code == 201

    category_id = create_response.get_json()["id"]

    # Rename the category.
    update_response = client.patch(
        f"/api/categories/{category_id}",
        json={"name": "Home"},
    )

    assert update_response.status_code == 200

    updated_category = update_response.get_json()

    assert updated_category["id"] == category_id
    assert updated_category["name"] == "Home"

    # Confirm the updated name was saved.
    list_response = client.get("/api/categories")

    assert list_response.status_code == 200

    categories = list_response.get_json()

    assert any(
        item["id"] == category_id and item["name"] == "Home"
        for item in categories
    )

def test_delete_category_preserves_task(client):
    """Deleting a category must not delete its assigned tasks."""

    # Create a category.
    category_response = client.post(
        "/api/categories",
        json={"name": "Shopping"},
    )

    assert category_response.status_code == 201
    category_id = category_response.get_json()["id"]

    # Create a task assigned to that category.
    task_response = client.post(
        "/api/tasks",
        json={
            "title": "Buy groceries",
            "category_id": category_id,
        },
    )

    assert task_response.status_code == 201
    task_id = task_response.get_json()["id"]

    # Delete the category.
    delete_response = client.delete(
        f"/api/categories/{category_id}"
    )

    assert delete_response.status_code == 204

    # Confirm the task still exists without a category.
    get_response = client.get(f"/api/tasks/{task_id}")

    assert get_response.status_code == 200

    saved_task = get_response.get_json()

    assert saved_task["title"] == "Buy groceries"
    assert saved_task["category_id"] is None

    # Confirm the deleted category is no longer listed.
    categories_response = client.get("/api/categories")

    assert categories_response.status_code == 200
    assert all(
        category["id"] != category_id
        for category in categories_response.get_json()
    )

def test_assign_category_to_task(client):
    """A task can be assigned to a category in PostgreSQL."""

    # Create a category for this test.
    category_response = client.post(
        "/api/categories",
        json={"name": "School"},
    )

    assert category_response.status_code == 201

    category_id = category_response.get_json()["id"]

    # Create a task assigned to that category.
    task_response = client.post(
        "/api/tasks",
        json={
            "title": "Complete Week 2 assignment",
            "category_id": category_id,
        },
    )

    assert task_response.status_code == 201

    task = task_response.get_json()

    assert task["title"] == "Complete Week 2 assignment"
    assert task["category_id"] == category_id

    # Retrieve the task to confirm the category was saved.
    saved_response = client.get(
        f"/api/tasks/{task['id']}"
    )

    assert saved_response.status_code == 200

    saved_task = saved_response.get_json()

    assert saved_task["category_id"] == category_id

def test_filter_tasks_by_category(client):
    """Filtering by category returns only matching tasks."""

    # Create two different categories.
    school_response = client.post(
        "/api/categories",
        json={"name": "School"},
    )

    work_response = client.post(
        "/api/categories",
        json={"name": "Work"},
    )

    assert school_response.status_code == 201
    assert work_response.status_code == 201

    school_id = school_response.get_json()["id"]
    work_id = work_response.get_json()["id"]

    # Create one task in each category.
    school_task = client.post(
        "/api/tasks",
        json={
            "title": "Complete homework",
            "category_id": school_id,
        },
    )

    work_task = client.post(
        "/api/tasks",
        json={
            "title": "Prepare meeting notes",
            "category_id": work_id,
        },
    )

    assert school_task.status_code == 201
    assert work_task.status_code == 201

    # Request only tasks in the School category.
    response = client.get(
        f"/api/tasks?category_id={school_id}"
    )

    assert response.status_code == 200

    tasks = response.get_json()

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Complete homework"
    assert tasks[0]["category_id"] == school_id

def test_filter_tasks_by_category_and_status(client):
    """Filter tasks by both category and completion status."""

    # Create two categories.
    school_response = client.post(
        "/api/categories",
        json={"name": "School"},
    )

    work_response = client.post(
        "/api/categories",
        json={"name": "Work"},
    )

    assert school_response.status_code == 201
    assert work_response.status_code == 201

    school_id = school_response.get_json()["id"]
    work_id = work_response.get_json()["id"]

    # Create an active School task.
    active_school = client.post(
        "/api/tasks",
        json={
            "title": "Study PostgreSQL",
            "category_id": school_id,
        },
    )

    # Create another School task.
    completed_school = client.post(
        "/api/tasks",
        json={
            "title": "Finish homework",
            "category_id": school_id,
        },
    )

    # Create an active Work task.
    active_work = client.post(
        "/api/tasks",
        json={
            "title": "Prepare meeting",
            "category_id": work_id,
        },
    )

    assert active_school.status_code == 201
    assert completed_school.status_code == 201
    assert active_work.status_code == 201

    # Mark one School task as completed.
    completed_id = completed_school.get_json()["id"]

    update_response = client.patch(
        f"/api/tasks/{completed_id}",
        json={"is_complete": True},
    )

    assert update_response.status_code == 200

    # Request only active School tasks.
    response = client.get(
        f"/api/tasks?status=active&category_id={school_id}"
    )

    assert response.status_code == 200

    tasks = response.get_json()

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Study PostgreSQL"
    assert tasks[0]["category_id"] == school_id
    assert tasks[0]["is_complete"] is False

# Authentication and account ownership tests

def test_missing_bearer_token_returns_401(client):
    response = client.get("/api/tasks", headers={"Authorization": ""})
    assert response.status_code == 401


def test_invalid_bearer_token_returns_401(client, monkeypatch):
    monkeypatch.setattr(task_app, "verify_access_token", lambda token: None)
    response = client.get("/api/tasks")
    assert response.status_code == 401


def test_auth_service_unavailable_returns_503(client, monkeypatch):
    def unavailable(token):
        raise ConnectionError("Simulated Supabase outage")

    monkeypatch.setattr(task_app, "verify_access_token", unavailable)
    response = client.get("/api/tasks")
    assert response.status_code == 503


def test_health_remains_public(client):
    response = client.get("/api/health", headers={"Authorization": ""})
    assert response.status_code == 200


def test_users_cannot_access_each_others_tasks(client, monkeypatch):
    created = client.post("/api/tasks", json={"title": "User A private task"})
    assert created.status_code == 201
    task_id = created.get_json()["id"]

    act_as(monkeypatch, SECOND_USER_ID)
    assert client.get(f"/api/tasks/{task_id}").status_code == 404
    assert client.get("/api/tasks").get_json() == []

    act_as(monkeypatch, TEST_USER_ID)
    assert client.get(f"/api/tasks/{task_id}").status_code == 200


def test_users_cannot_update_each_others_tasks(client, monkeypatch):
    created = client.post("/api/tasks", json={"title": "User A original task"})
    assert created.status_code == 201
    task_id = created.get_json()["id"]

    act_as(monkeypatch, SECOND_USER_ID)
    response = client.patch(
        f"/api/tasks/{task_id}", json={"title": "Changed by User B"}
    )
    assert response.status_code == 404

    act_as(monkeypatch, TEST_USER_ID)
    original = client.get(f"/api/tasks/{task_id}")
    assert original.status_code == 200
    assert original.get_json()["title"] == "User A original task"


def test_users_cannot_delete_each_others_tasks(client, monkeypatch):
    created = client.post("/api/tasks", json={"title": "Keep User A task"})
    assert created.status_code == 201
    task_id = created.get_json()["id"]

    act_as(monkeypatch, SECOND_USER_ID)
    assert client.delete(f"/api/tasks/{task_id}").status_code == 404

    act_as(monkeypatch, TEST_USER_ID)
    assert client.get(f"/api/tasks/{task_id}").status_code == 200


def test_users_cannot_access_each_others_categories(client, monkeypatch):
    created = client.post("/api/categories", json={"name": "Private category"})
    assert created.status_code == 201
    category_id = created.get_json()["id"]

    act_as(monkeypatch, SECOND_USER_ID)
    categories = client.get("/api/categories")
    assert categories.status_code == 200
    assert categories.get_json() == []
    assert client.patch(
        f"/api/categories/{category_id}", json={"name": "Stolen"}
    ).status_code == 404
    assert client.delete(f"/api/categories/{category_id}").status_code == 404

    act_as(monkeypatch, TEST_USER_ID)
    categories = client.get("/api/categories").get_json()
    assert any(item["id"] == category_id and item["name"] == "Private category"
               for item in categories)


def test_users_cannot_assign_others_categories(client, monkeypatch):
    created = client.post("/api/categories", json={"name": "User A category"})
    assert created.status_code == 201
    category_id = created.get_json()["id"]

    act_as(monkeypatch, SECOND_USER_ID)
    response = client.post(
        "/api/tasks", json={"title": "Invalid association", "category_id": category_id}
    )
    assert response.status_code in (400, 404)
    assert client.get("/api/tasks").get_json() == []


def test_users_cannot_reassign_tasks_to_others_categories(client, monkeypatch):
    category = client.post("/api/categories", json={"name": "User A category"})
    assert category.status_code == 201
    category_id = category.get_json()["id"]

    act_as(monkeypatch, SECOND_USER_ID)
    task = client.post("/api/tasks", json={"title": "User B task"})
    assert task.status_code == 201
    task_id = task.get_json()["id"]
    response = client.patch(
        f"/api/tasks/{task_id}", json={"category_id": category_id}
    )
    assert response.status_code in (400, 404)
    assert client.get(f"/api/tasks/{task_id}").get_json()["category_id"] is None


def test_same_category_name_allowed_for_different_users(client, monkeypatch):
    first = client.post("/api/categories", json={"name": "Work"})
    assert first.status_code == 201

    act_as(monkeypatch, SECOND_USER_ID)
    second = client.post("/api/categories", json={"name": "Work"})
    assert second.status_code == 201
    assert second.get_json()["id"] != first.get_json()["id"]


def test_reject_client_supplied_task_owner(client):
    response = client.post(
        "/api/tasks",
        json={"title": "Forged owner", "user_id": str(SECOND_USER_ID)},
    )
    assert response.status_code == 400


def test_reject_client_supplied_category_owner(client):
    response = client.post(
        "/api/categories",
        json={"name": "Forged owner", "user_id": str(SECOND_USER_ID)},
    )
    assert response.status_code == 400


def test_invalid_mixed_patch_does_not_change_task(client):
    created = client.post("/api/tasks", json={"title": "Original"})
    assert created.status_code == 201
    task_id = created.get_json()["id"]
    response = client.patch(
        f"/api/tasks/{task_id}",
        json={"title": "Changed", "is_complete": "false"},
    )
    assert response.status_code == 400
    saved = client.get(f"/api/tasks/{task_id}").get_json()
    assert saved["title"] == "Original"
    assert saved["is_complete"] is False
