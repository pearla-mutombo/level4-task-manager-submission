
"""Helper functions for the Task Manager's in-memory storage."""


def create_initial_tasks():
    """Return a fresh list containing the two starting tasks."""

    return [
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


def find_task(tasks, task_id):
    """Find a task by its ID in the supplied list."""

    for task in tasks:
        if task["id"] == task_id:
            return task

    # Return None if no task has the requested ID.
    return None
