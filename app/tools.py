import json
from langchain_core.tools import tool
from typing import List, Dict, Any
import os
from pathlib import Path
from datetime import datetime, timedelta
import re

# File-based storage for persistence
STORAGE_FILE = Path(__file__).parent.parent / "storage.json"

class StorageManager:
    def __init__(self):
        self.storage_file = STORAGE_FILE
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Ensure storage file exists with default structure"""
        if not self.storage_file.exists():
            default_data = {
                "conversation_history": [],
                "todo_list": [],
                "user_name": None
            }
            self._save_data(default_data)
    
    def _load_data(self):
        """Load data from storage file"""
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading storage: {e}")
            return {"conversation_history": [], "todo_list": [], "user_name": None}
    
    def _save_data(self, data):
        """Save data to storage file"""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving storage: {e}")
    
    def get_todos(self):
        """Get all todos"""
        data = self._load_data()
        return data.get("todo_list", [])
    
    def add_todo(self, todo, priority="medium", due_date=None):
        """Add a todo with optional priority and due date"""
        data = self._load_data()
        todo_item = {
            "task": todo,
            "priority": priority,
            "due_date": due_date,
            "created_at": datetime.now().isoformat(),
            "completed": False,
            "id": len(data["todo_list"]) + 1
        }
        data["todo_list"].append(todo_item)
        self._save_data(data)
        return todo_item
    
    def remove_todo(self, index):
        """Remove a todo by index"""
        data = self._load_data()
        todo_list = data.get("todo_list", [])
        if 0 <= index < len(todo_list):
            removed = todo_list.pop(index)
            self._save_data(data)
            return removed
        return None
    
    def complete_todo(self, index):
        """Mark a todo as completed"""
        data = self._load_data()
        todo_list = data.get("todo_list", [])
        if 0 <= index < len(todo_list):
            todo_list[index]["completed"] = True
            todo_list[index]["completed_at"] = datetime.now().isoformat()
            self._save_data(data)
            return todo_list[index]
        return None
    
    def save_user_name(self, name):
        """Save user name"""
        data = self._load_data()
        data["user_name"] = name
        self._save_data(data)
    
    def get_user_name(self):
        """Get user name"""
        data = self._load_data()
        return data.get("user_name")
    
    def get_analytics(self):
        """Get todo analytics"""
        data = self._load_data()
        todos = data.get("todo_list", [])
        total = len(todos)
        completed = len([t for t in todos if t.get("completed", False)])
        pending = total - completed
        
        # Priority breakdown
        priority_counts = {"high": 0, "medium": 0, "low": 0}
        for todo in todos:
            priority = todo.get("priority", "medium")
            if priority in priority_counts:
                priority_counts[priority] += 1
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": round((completed / total * 100) if total > 0 else 0, 1),
            "priority_breakdown": priority_counts
        }

# Global storage manager instance
storage = StorageManager()

@tool
def add_todo(todo: str, priority: str = "medium"):
    """
    Adds a new item to the to-do list with priority detection.
    Args:
        todo: The task to add to the list.
        priority: Priority level (high, medium, low). Default is medium.
    """
    try:
        # Parse priority from the todo text if mentioned
        priority_patterns = {
            "high": r"\b(urgent|important|high|asap|critical|priority)\b",
            "low": r"\b(low|later|someday|optional|maybe)\b"
        }
        
        for p, pattern in priority_patterns.items():
            if re.search(pattern, todo.lower()):
                priority = p
                break
        
        todo_item = storage.add_todo(todo, priority)
        priority_emoji = {"high": "🔥", "medium": "⚡", "low": "📝"}
        return f"✅ Successfully added '{todo}' to your to-do list with {priority_emoji.get(priority, '⚡')} {priority} priority!"
    except Exception as e:
        return f"❌ Error adding todo: {str(e)}"

@tool
def remove_todo(todo_index: int):
    """
    Removes an item from the to-do list by its index.
    Args:
        todo_index: The 1-based index of the task to remove.
    """
    try:
        todos = storage.get_todos()
        if 1 <= todo_index <= len(todos):
            removed_todo = storage.remove_todo(todo_index - 1)
            if removed_todo:
                task_name = removed_todo.get("task", removed_todo) if isinstance(removed_todo, dict) else removed_todo
                return f"🗑️ Successfully removed '{task_name}' from your to-do list."
            else:
                return "❌ Error: Could not remove the todo item."
        else:
            return f"❌ Error: Invalid index. Please provide a number between 1 and {len(todos)}."
    except Exception as e:
        return f"❌ Error removing todo: {str(e)}"

@tool
def complete_todo(todo_index: int):
    """
    Marks a todo item as completed.
    Args:
        todo_index: The 1-based index of the task to complete.
    """
    try:
        todos = storage.get_todos()
        if 1 <= todo_index <= len(todos):
            completed_todo = storage.complete_todo(todo_index - 1)
            if completed_todo:
                task_name = completed_todo.get("task", "task")
                return f"🎉 Congratulations! You completed '{task_name}'!"
            else:
                return "❌ Error: Could not mark the todo as completed."
        else:
            return f"❌ Error: Invalid index. Please provide a number between 1 and {len(todos)}."
    except Exception as e:
        return f"❌ Error completing todo: {str(e)}"

@tool
def list_todos():
    """
    Lists all items currently in the to-do list with enhanced formatting.
    """
    try:
        todo_list = storage.get_todos()
        if not todo_list:
            return "📝 Your to-do list is empty. Ready to add some tasks?"
        
        formatted_items = []
        for i, todo in enumerate(todo_list):
            if isinstance(todo, dict):
                task = todo.get("task", "Unknown task")
                priority = todo.get("priority", "medium")
                completed = todo.get("completed", False)
                due_date = todo.get("due_date")
                
                # Priority and status emojis
                priority_emoji = {"high": "🔥", "medium": "⚡", "low": "📝"}
                status_emoji = "✅" if completed else "⏳"
                
                item_text = f"{status_emoji} {i+1}. {task} {priority_emoji.get(priority, '⚡')}"
                if due_date:
                    item_text += f" (Due: {due_date})"
                if completed:
                    item_text += " ✨"
                    
                formatted_items.append(item_text)
            else:
                formatted_items.append(f"⏳ {i+1}. {todo}")
        
        return f"📋 **Your To-Do List:**\n\n" + "\n".join(formatted_items)
    except Exception as e:
        return f"❌ Error listing todos: {str(e)}"

@tool
def get_analytics():
    """
    Provides detailed analytics about your to-do list and productivity.
    """
    try:
        analytics = storage.get_analytics()
        
        report = f"""📊 **Productivity Analytics:**

📈 **Overview:**
• Total Tasks: {analytics['total']}
• Completed: {analytics['completed']} ✅
• Pending: {analytics['pending']} ⏳
• Completion Rate: {analytics['completion_rate']}% 

🎯 **Priority Breakdown:**
• High Priority: {analytics['priority_breakdown']['high']} 🔥
• Medium Priority: {analytics['priority_breakdown']['medium']} ⚡
• Low Priority: {analytics['priority_breakdown']['low']} 📝

💡 **Insights:**"""
        
        if analytics['completion_rate'] >= 80:
            report += "\n• 🌟 Excellent productivity! You're crushing your goals!"
        elif analytics['completion_rate'] >= 50:
            report += "\n• 👍 Good progress! Keep up the momentum!"
        else:
            report += "\n• 💪 You can do it! Focus on completing pending tasks!"
            
        if analytics['priority_breakdown']['high'] > 0:
            report += f"\n• ⚠️ You have {analytics['priority_breakdown']['high']} high-priority tasks!"
            
        return report
    except Exception as e:
        return f"❌ Error generating analytics: {str(e)}"

@tool
def search_todos(keyword: str):
    """
    Searches for todos containing a specific keyword.
    Args:
        keyword: The keyword to search for in tasks.
    """
    try:
        todos = storage.get_todos()
        matching_todos = []
        
        for i, todo in enumerate(todos):
            task_text = todo.get("task", todo) if isinstance(todo, dict) else todo
            if keyword.lower() in task_text.lower():
                status = "✅" if isinstance(todo, dict) and todo.get("completed") else "⏳"
                matching_todos.append(f"{status} {i+1}. {task_text}")
        
        if not matching_todos:
            return f"🔍 No tasks found containing '{keyword}'"
        
        return f"🔍 **Search Results for '{keyword}':**\n\n" + "\n".join(matching_todos)
    except Exception as e:
        return f"❌ Error searching todos: {str(e)}"

@tool
def get_motivational_quote():
    """
    Provides a motivational quote to boost productivity.
    """
    quotes = [
        "🌟 'The way to get started is to quit talking and begin doing.' - Walt Disney",
        "💪 'Success is not final, failure is not fatal: it is the courage to continue that counts.' - Winston Churchill",
        "🚀 'Don't watch the clock; do what it does. Keep going.' - Sam Levenson",
        "⭐ 'The future depends on what you do today.' - Mahatma Gandhi",
        "🎯 'You are never too old to set another goal or to dream a new dream.' - C.S. Lewis",
        "💫 'Believe you can and you're halfway there.' - Theodore Roosevelt",
        "🎪 'It is during our darkest moments that we must focus to see the light.' - Aristotle",
        "🌈 'The only impossible journey is the one you never begin.' - Tony Robbins"
    ]
    
    import random
    return random.choice(quotes)

@tool
def set_reminder(task: str, minutes: int):
    """
    Sets a reminder for a task (simulated for demo purposes).
    Args:
        task: The task to be reminded about.
        minutes: Number of minutes until reminder.
    """
    try:
        reminder_time = datetime.now() + timedelta(minutes=minutes)
        return f"⏰ Reminder set! I'll remind you about '{task}' at {reminder_time.strftime('%H:%M')} (in {minutes} minutes)."
    except Exception as e:
        return f"❌ Error setting reminder: {str(e)}"

@tool
def save_user_name(name: str):
    """
    Saves the user's name for personalized experience.
    Args:
        name: The user's name.
    """
    try:
        storage.save_user_name(name)
        return f"🙋‍♂️ Thanks, {name}! I'll remember that and personalize our conversations."
    except Exception as e:
        return f"❌ Error saving name: {str(e)}"

@tool
def get_user_name():
    """
    Retrieves the saved user's name.
    """
    try:
        name = storage.get_user_name()
        if name:
            return f"👋 Your name is {name}."
        else:
            return "🤔 I don't know your name yet. What should I call you?"
    except Exception as e:
        return f"❌ Error retrieving name: {str(e)}"

@tool
def clear_todos():
    """
    Clears all items from the to-do list.
    """
    try:
        data = storage._load_data()
        data["todo_list"] = []
        storage._save_data(data)
        return "🧹 Successfully cleared all items from your to-do list. Fresh start!"
    except Exception as e:
        return f"❌ Error clearing todos: {str(e)}"

@tool
def count_todos():
    """
    Returns detailed count information about the to-do list.
    """
    try:
        todos = storage.get_todos()
        total = len(todos)
        completed = len([t for t in todos if isinstance(t, dict) and t.get("completed", False)])
        pending = total - completed
        
        if total == 0:
            return "📝 Your to-do list is empty. Ready to add some tasks?"
        
        result = f"📊 **Task Summary:**\n"
        result += f"• Total: {total} tasks\n"
        result += f"• Completed: {completed} ✅\n"
        result += f"• Pending: {pending} ⏳\n"
        
        if total > 0:
            completion_rate = round((completed / total) * 100, 1)
            result += f"• Progress: {completion_rate}% complete"
            
            if completion_rate >= 80:
                result += " 🌟 Excellent!"
            elif completion_rate >= 50:
                result += " 👍 Good progress!"
            else:
                result += " 💪 Keep going!"
        
        return result
    except Exception as e:
        return f"❌ Error counting todos: {str(e)}"
