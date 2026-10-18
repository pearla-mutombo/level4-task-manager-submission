"""Practice Python values without changing the task-manager server."""

tasks = [
    {"id": 1, "title": "Learn Python values", "is_complete": False},
    {"id": 2, "title": "Open Postman", "is_complete": True},
]

# Add the requested print statements and dictionary/list changes here.
print("Predict each result, then complete the steps in README.md.")
# Exercise 1: Print the title of the first task
print("First task:", tasks[0]["title"])

# Exercise 2: Print the completion status of the second task
print("Second task completed:", tasks[1]["is_complete"])

# Excercise 3: Count how many tasks are in the list
print("Total tasks:", len(tasks))
# tasks is the list containing our task dictionaries.
# len() counts how many items are in that list.
# print() displays the result.

# Excercise 4: Update the title of the firs task.
tasks[0]["title"] = "Practice Python dictionaries"

# Display the updated title
print("Updated first task:", tasks[0]["title"])
# tasks[0] selects the first task.
# ["title"] identifies the value we want to change.
# = assigns a new value.
# "Preactice Python dictionaries" is the new title.

# Exercise 5: Add a third task to the list
tasks.append({
    "id": 3,
    "title": "Practice Flask API",
    "is_complete": False
})

# Display the new tasks and the updated number of tasks
print("Third task:", tasks[2]["title"])
print("Total tasks after adding:", len(tasks))
# tasks.append() adds a new item to the end of the list
# "id": 3 gives the new task an ID.
# "title" stores the task's description.
# "is_complete": False means the task hasn't been completed.
# tasks[2] accesses the third task because Python starts counting at zero.
# len(tasks) confirms that the list now contains three tasks.

# Exercise 6: Identify different Python data types

# String: stores text
print("String type:", type("Learn Python"))

# Integer: stores whole numbers
print("Integer type:", type(3))

# Boolean: stores True or False
print("Boolean type:", type(False))

# List: stores multiple items
print("List type:", type(tasks))

# Dictionary: stores key-value pairs
print("Dictionary type:", type(tasks[0]))

# What does type() do?
# "Learn Python" = str(sting)
# 3 = int(integer)
# False = bool(Boolean)
# tasks = list
# tasks[0] = dict(dictionary)

# Exercise 7: Python Boolean values versus JSON Boolean values
#
# Python uses True and False with capital first letters.
# JSON uses true and false with lowercase letters.
#
# Example in Python:
# is_complete = False
#
# Example in JSON:
# {"is_complete": false}
#
# Both represent Boolean values, but they use different syntax.