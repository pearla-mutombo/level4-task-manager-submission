"""Separate file/JSON practice. This does not persist task-manager data."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DATA = PROJECT_ROOT / "sample-data"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"

# Use with/open (or Path.read_text), json.load/json.loads, and json.dump/json.dumps.
# Read reading-list.json; write an edited copy under OUTPUT_DIR.
# Handle FileNotFoundError and json.JSONDecodeError in separate examples.
print("Sample files:", SAMPLE_DATA)
print("Complete the read/write/error steps in README.md.")
