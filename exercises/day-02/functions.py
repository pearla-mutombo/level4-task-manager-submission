
"""Day 2: Practice Python functions, loops, and conditions."""

# A list containing two task dictionaries.
tasks = [
    {"id": 1, "title": "Practice loops", "is_complete": False},
    {"id": 2, "title": "Understand functions", "is_complete": True},
]


# Function 1: Find all incomplete tasks.
def get_active_tasks(tasks):
    active_tasks = []

    # Go through each task in the list.
    for task in tasks:
        # Add the task if it is not complete.
        if task["is_complete"] == False:
            active_tasks.append(task)

    return active_tasks


# Function 2: Find one task by its ID.
def find_task(tasks, task_id):
    # Check each task in the list.
    for task in tasks:
        if task["id"] == task_id:
            return task

    # No matching task was found.
    return None


# Function 3: Remove spaces from a title.
def clean_title(title):
    return title.strip()


# Call each function to demonstrate its results.
print("Active tasks:", get_active_tasks(tasks))
print("Existing task:", find_task(tasks, 1))
print("Missing task:", find_task(tasks, 99))
print("Clean title:", clean_title("   Learn Python functions   "))
