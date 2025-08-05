import json
from langchain_core.tools import tool
from typing import List

STORAGE_FILE = "storage.json"

def load_storage():
    try:
        with open(STORAGE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'conversation_history': [], 'todo_list': []}

def save_storage(data):
    with open(STORAGE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@tool
def add_todo(todo: str):
    """
    Adds a new item to the to-do list.
    Args:
        todo: The task to add to the list.
    """
    storage = load_storage()
    storage['todo_list'].append(todo)
    save_storage(storage)
    return f"Successfully added '{todo}' to your to-do list."

@tool
def remove_todo(todo_index: int):
    """
    Removes an item from the to-do list by its index.
    Args:
        todo_index: The 1-based index of the task to remove.
    """
    storage = load_storage()
    if 0 < todo_index <= len(storage['todo_list']):
        removed_todo = storage['todo_list'].pop(todo_index - 1)
        save_storage(storage)
        return f"Successfully removed '{removed_todo}' from your to-do list."
    return "Error: Invalid index. Please provide a valid number from the list."

@tool
def list_todos():
    """
    Lists all items currently in the to-do list.
    """
    storage = load_storage()
    if not storage['todo_list']:
        return "Your to-do list is empty."
    
    formatted_list = "\n".join(f"{i+1}. {todo}" for i, todo in enumerate(storage['todo_list']))
    return f"Here is your current to-do list:\n{formatted_list}"
