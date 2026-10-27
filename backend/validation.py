
"""Validation helpers for the Task Manager API."""

from flask import request
from werkzeug.exceptions import BadRequest


def read_json_object():
    """Read a request body and verify it contains a JSON object."""

    # The request must use a JSON content type.
    if not request.is_json:
        return None, "Send the request body as application/json.", 415

    try:
        data = request.get_json()
    except BadRequest:
        return None, "Request body must be valid JSON.", 400

    # A task request must contain a JSON object, not a list.
    if not isinstance(data, dict):
        return None, "Request body must be a JSON object.", 400

    return data, None, None


def validate_title(value):
    """Require a title containing between 1 and 80 characters."""

    # A task title must be a string.
    if not isinstance(value, str):
        return None, "Title must be a string."

    # Remove extra spaces from the beginning and end.
    title = value.strip()

    if not 1 <= len(title) <= 80:
        return None, "Title must contain between 1 and 80 characters."

    return title, None
