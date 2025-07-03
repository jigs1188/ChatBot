
import json
from langchain_core.tools import tool
from typing import List

TODO_FILE = "todolist.json"

def get_todos() -> List[str]:
    """Reads the to-do list from the JSON file."""
    try:
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@tool
def add_todo(todo: str):
    """
    Adds a new item to the to-do list.
    Args:
        todo: The task to add to the list.
    """
    todos = get_todos()
    todos.append(todo)
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=4)
    return f"Successfully added '{todo}' to your to-do list."

@tool
def remove_todo(todo_index: int):
    """
    Removes an item from the to-do list by its index.
    Args:
        todo_index: The 1-based index of the task to remove.
    """
    todos = get_todos()
    if 0 < todo_index <= len(todos):
        removed_todo = todos.pop(todo_index - 1)
        with open(TODO_FILE, "w") as f:
            json.dump(todos, f, indent=4)
        return f"Successfully removed '{removed_todo}' from your to-do list."
    return "Error: Invalid index. Please provide a valid number from the list."

@tool
def list_todos():
    """
    Lists all items currently in the to-do list.
    """
    todos = get_todos()
    if not todos:
        return "Your to-do list is empty."
    
    formatted_list = "\n".join(f"{i+1}. {todo}" for i, todo in enumerate(todos))
    return f"Here is your current to-do list:\n{formatted_list}"
