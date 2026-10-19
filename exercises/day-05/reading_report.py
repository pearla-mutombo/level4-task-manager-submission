"""Day 5: Read a JSON reading list and create a text report."""

import json
from pathlib import Path

from report_utils import count_books, get_book_titles


# Find the project folder using the location of this Python file.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# The original JSON file we will read.
INPUT_FILE = PROJECT_ROOT / "sample-data" / "reading-list.json"

# The text file our program will create.
OUTPUT_FILE = PROJECT_ROOT / "exercises" / "day-05" / "reading-report.txt"


def load_books():
    """Read the JSON file and return its list of books."""
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        books = json.load(file)

    if not isinstance(books, list):
        raise ValueError("The reading list must contain a JSON list.")

    return books


def create_report(books):
    """Build a text report using our imported helper functions."""
    total = count_books(books)
    titles = get_book_titles(books)

    lines = [
        "MY READING LIST REPORT",
        "======================",
        f"Total books: {total}",
        "",
        "Book titles:",
    ]

    for number, title in enumerate(titles, start=1):
        lines.append(f"{number}. {title}")

    return "\n".join(lines)


def save_report(report):
    """Write the completed report to a text file."""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(report + "\n")


def main():
    """Run the reading list report program."""
    try:
        books = load_books()
        report = create_report(books)
        save_report(report)

        print(report)
        print()
        print(f"Report saved to: {OUTPUT_FILE}")

    except FileNotFoundError:
        print("Error: The reading list JSON file was not found.")

    except json.JSONDecodeError:
        print("Error: The reading list contains invalid JSON.")

    except (ValueError, KeyError, TypeError) as error:
        print(f"Error: Invalid reading list data: {error}")


if __name__ == "__main__":
    main()

# What is reading_report.py supposed to do?
# imagine you have a notebook containing a list of books you've been reading.
# Instead of counting those books and writing a summary yourself, you create a Python
# program that does the work automatically.
# 1. Read the JSON file --> sample-data/reading-list.json
# 2. Process the book information --> Count books and collect their titles
# 3. Create a text report --> exercise/day-05/reading-report.txt
# 4. Display the results in Terminal

# Each imports has a different purpose
# import                            what it does?
# json                Allows the pyton to read JSON files and convert their contents into Python
# Path                Helps Python find files and folders on your computer
# count_books         Imports your own function that counts books
# get_book_titlee     Imports your own function that collects book titles
# * I created report_utils.py, and now reading_report.py can resuse its function without writing the same code twice.
# Think of INPUT_FILE as the book you're reading from, and OUTPUT_FILE as the paper you're writing your summary on.
# the expresson parents[2] goes up three folder levels from reading-report.py to reach the project folder.

# 1. def load_books(): creates a function named load_books.
# 2. open(..., "r") opens the file in read mode. The "r" means read.
# 3. json.load(file) converts the JSON content into Python data.
# 4. isinstance(books, list) checks whether the data is a list.
# 5. return books gives the book information back to the rest of the program.

# Here is what the finish report will look like:
# MY READING LIST REPORT
# ======================
# Total books: 2

# Book titles:
# 1. Python Basics
# 2. Learning Flask

# For my Day 5 assignment, I created a Python program that reads book information
# from a JSON file and generates a text report. I organize my code into functions so
# each function has a specific responsibility. I also created a separate Python module
# called report_utils.py and imported two functions from it to count the books and
# collect their titles. My program includes error handling for missing files and invalid
# data, and it saves the report withour modifying the orginal JSON file.
