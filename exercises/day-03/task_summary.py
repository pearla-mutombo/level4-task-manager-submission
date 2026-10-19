
"""Day 3: Task Summary - Python Fundamentals."""

# A list of dictionaries representing our tasks.
tasks = [
    {"id": 1, "title": "Practice Python loops", "is_complete": True},
    {"id": 2, "title": "Learn Python functions", "is_complete": True},
    {"id": 3, "title": "Practice Flask CRUD", "is_complete": False},
    {"id": 4, "title": "Write Day 3 README", "is_complete": False},
]


# Function 1: Count the completed tasks.
def count_completed_tasks(task_list):
    completed = 0

    # Check each task in the list.
    for task in task_list:
        if task["is_complete"] == True:
            completed += 1

    return completed


# Function 2: Count the incomplete tasks.
def count_incomplete_tasks(task_list):
    incomplete = 0

    # Check each task in the list.
    for task in task_list:
        if task["is_complete"] == False:
            incomplete += 1

    return incomplete


# Function 3: Print a summary of the tasks.
def print_task_summary(task_list):
    completed = count_completed_tasks(task_list)
    incomplete = count_incomplete_tasks(task_list)
    total = len(task_list)

    print("===== DAY 3 TASK SUMMARY =====")
    print("Total tasks:", total)
    print("Completed tasks:", completed)
    print("Incomplete tasks:", incomplete)
    print("==============================")


# Call the function to display the results.
print_task_summary(tasks)
