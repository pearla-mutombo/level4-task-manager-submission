
"""Day 4: Practice reading, writing, and handling JSON files."""

import json
from pathlib import Path

# Find the project and exercise folders.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DATA = PROJECT_ROOT / "sample-data"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def read_json_file(file_path):
    """Read a JSON file and return its Python data."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json_file(file_path, data):
    """Save Python data into a JSON file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def main():
    # Step 1: Read the original reading list.
    reading_list = read_json_file(
        SAMPLE_DATA / "reading-list.json"
    )

    # Step 2: Display the first book.
    print("First book:", reading_list[0]["title"])

    # Step 3: Add a new book.
    new_book = {
        "id": 3,
        "title": "Learning Python JSON",
        "finished": False,
    }

    reading_list.append(new_book)

    # Step 4: Save a separate copy.
    output_file = OUTPUT_DIR / "reading-list.json"
    save_json_file(output_file, reading_list)

    print("Updated reading list saved successfully!")
    print("Total books:", len(reading_list))

    # Step 5: Handle a missing file.
    try:
        read_json_file(SAMPLE_DATA / "missing.json")
    except FileNotFoundError:
        print("FileNotFoundError handled: File not found.")

    # Step 6: Handle invalid JSON.
    try:
        read_json_file(SAMPLE_DATA / "malformed.json")
    except json.JSONDecodeError:
        print("JSONDecodeError handled: Invalid JSON format.")


if __name__ == "__main__":
    main()

