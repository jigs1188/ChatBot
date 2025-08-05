import json
import redis
from langchain_core.tools import tool
from typing import List
import os

# Connect to Redis
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.from_url(redis_url)

@tool
def add_todo(todo: str):
    """
    Adds a new item to the to-do list.
    Args:
        todo: The task to add to the list.
    """
    r.rpush("todo_list", todo)
    return f"Successfully added '{todo}' to your to-do list."

@tool
def remove_todo(todo_index: int):
    """
    Removes an item from the to-do list by its index.
    Args:
        todo_index: The 1-based index of the task to remove.
    """
    if 0 < todo_index <= r.llen("todo_list"):
        removed_todo = r.lindex("todo_list", todo_index - 1).decode("utf-8")
        r.lrem("todo_list", 1, r.lindex("todo_list", todo_index - 1))
        return f"Successfully removed '{removed_todo}' from your to-do list."
    return "Error: Invalid index. Please provide a valid number from the list."

@tool
def list_todos():
    """
    Lists all items currently in the to-do list.
    """
    todo_list = [item.decode("utf-8") for item in r.lrange("todo_list", 0, -1)]
    if not todo_list:
        return "Your to-do list is empty."
    
    formatted_list = "\n".join(f"{i+1}. {todo}" for i, todo in enumerate(todo_list))
    return f"Here is your current to-do list:\n{formatted_list}"

@tool
def save_user_name(name: str):
    """
    Saves the user's name.
    Args:
        name: The user's name.
    """
    r.set("user_name", name)
    return f"Thanks, {name}! I'll remember that."
