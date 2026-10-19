"""Helper functions for the Day 5 reading list report."""


def count_books(books):
    """Count how many books are in the reading list."""
    return len(books)


def get_book_titles(books):
    """Create a list containing the title of each book."""
    titles = []

    for book in books:
        titles.append(book["title"])

    return titles