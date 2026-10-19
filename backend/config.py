
"""Configuration settings for the Flask Task Manager."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Locate the backend folder.
BASE_DIR = Path(__file__).resolve().parent

# Load environment settings from backend/.env, if it exists.
load_dotenv(BASE_DIR / ".env")


def get_frontend_origin():
    """Return the React application's allowed origin."""
    return os.getenv(
        "FRONTEND_ORIGIN",
        "http://127.0.0.1:5173",
    )
# What this code does
# load_dotenv() reads settings from a .env file if one exists.
# os.getenv() retrieves the FRONTED_ORIGIN setting.
# if the setting isn't provided, Pythin uses http://127.0.0.1:5173 as the default.
# get_frontend_origin() is a reusable function that we can import into app.py
# This shows to move a function into another Python file and import it.