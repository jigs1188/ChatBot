"""
Rex AI Assistant - Enterprise-Grade AI Productivity Platform

A professional Flask application that provides an AI-powered productivity assistant
with Progressive Web App (PWA) capabilities, mobile-first design, and comprehensive
todo management features.

Features:
- AI chat interface with OpenRouter API integration
- Mobile-responsive PWA with offline functionality
- Advanced todo management with analytics
- Professional glassmorphism UI design
- Cross-platform compatibility

Author: Rex AI Assistant Team
License: MIT
Version: 1.0.0
"""

import json
import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
import traceback
import requests
from datetime import datetime
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application with professional configuration
app = Flask(__name__)

# Configure file-based storage paths
STORAGE_FILE = Path(__file__).parent / "storage.json"
TODO_FILE = Path(__file__).parent / "todolist.json"


def init_storage():
    """
    Initialize storage files with default data structure.

    Creates JSON files for storing conversation history, user data, and analytics
    if they don't already exist. This ensures the application has proper data
    persistence from the first run.

    Files created:
    - storage.json: Main application data including conversation history and analytics
    - todolist.json: Todo items and user preferences
    """
    if not STORAGE_FILE.exists():
        initial_data = {
            "conversation_history": [],
            "user_name": None,
            "analytics": {
                "total_tasks_created": 0,
                "total_tasks_completed": 0,
                "total_conversations": 0,
                "most_productive_day": None,
                "average_tasks_per_day": 0,
                "completion_rate": 0,
                "last_activity": None,
            },
        }
        save_data(STORAGE_FILE, initial_data)

    if not TODO_FILE.exists():
        save_data(TODO_FILE, {"todos": [], "user_name": None})


def load_data(file_path):
    """
    Load data from a JSON file with error handling.

    Args:
        file_path (Path): Path to the JSON file to load

    Returns:
        dict: Loaded data from JSON file, empty dict on error

    Error Handling:
        - Returns empty dict if file doesn't exist
        - Logs errors and returns empty dict on JSON parsing errors
        - Handles file permission and encoding issues gracefully
    """
    try:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return {}


def save_data(file_path, data):
    """
    Save data to a JSON file with proper formatting and error handling.

    Args:
        file_path (Path): Path where JSON data should be saved
        data (dict): Data to serialize and save to JSON

    Features:
        - Uses proper indentation (2 spaces) for readability
        - Ensures ASCII compatibility with ensure_ascii=False for international chars
        - Comprehensive error handling with logging
        - UTF-8 encoding for proper character support
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving data to {file_path}: {e}")


def get_ai_response(user_input):
    """
    Generate AI responses using OpenRouter API with intelligent fallbacks.

    This function implements a robust AI response system with multiple layers:
    1. Primary: OpenRouter API with DeepSeek model
    2. Fallback: Intelligent pattern-based responses
    3. Error handling: Graceful degradation with helpful messages

    Args:
        user_input (str): User's message/query

    Returns:
        str: AI-generated response or intelligent fallback

    Features:
        - Integration with OpenRouter API for advanced AI responses
        - Intelligent fallback responses for common queries
        - Todo management integration through natural language
        - Error handling with user-friendly messages
        - Context-aware response generation
    """
    try:
        # Try OpenRouter API first
        api_key = os.getenv("OPENROUTER_API_KEY")
        if api_key:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

            data = {
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are Rex, an intelligent AI assistant. You help users with conversations, tasks, creativity, coding, and productivity. Be helpful, friendly, and concise. You can also manage todos - when users mention adding tasks, help them organize their work.",
                    },
                    {"role": "user", "content": user_input},
                ],
            }

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]

        # Fallback to intelligent rule-based responses
        return get_intelligent_response(user_input)

    except Exception as e:
        print(f"Error getting AI response: {e}")
        return get_intelligent_response(user_input)


def get_intelligent_response(user_input):
    """Intelligent rule-based responses for core functionality"""
    user_lower = user_input.lower()

    # Todo management
    if any(word in user_lower for word in ["add todo", "add task", "todo", "task"]):
        if "add" in user_lower or "create" in user_lower:
            # Extract task from input
            task = user_input
            for phrase in [
                "add todo:",
                "add task:",
                "todo:",
                "task:",
                "add a todo",
                "add a task",
            ]:
                if phrase in user_lower:
                    task = user_input[
                        user_input.lower().find(phrase) + len(phrase) :
                    ].strip()
                    break

            if task and task != user_input:
                add_todo_to_storage(task)
                return f"✅ Added todo: '{task}'. You now have {get_todo_count()} todos in your list!"
            else:
                return "📝 I'd be happy to add a todo for you! Please tell me what task you'd like to add. For example: 'Add todo: Buy groceries'"

        elif "list" in user_lower or "show" in user_lower:
            todos = get_todos()
            if todos:
                todo_list = "\n".join([f"• {todo['task']}" for todo in todos])
                return (
                    f"📋 **Your Todo List:**\n{todo_list}\n\n({len(todos)} items total)"
                )
            else:
                return "📝 Your todo list is empty! Add some tasks to get started."

    # Greeting responses
    if any(
        word in user_lower
        for word in ["hello", "hi", "hey", "good morning", "good afternoon"]
    ):
        data = load_data(STORAGE_FILE)
        user_name = data.get("user_name", "")
        greeting = f"Hello {user_name}! " if user_name else "Hello! "
        return f"👋 {greeting}I'm Rex, your AI assistant. I can help with conversations, manage your todos, assist with coding, creative writing, and much more! What would you like to work on today?"

    # Mobile/UI specific
    if any(
        word in user_lower
        for word in ["mobile", "responsive", "ui", "design", "beautiful"]
    ):
        return "📱 Thank you! This mobile interface features glassmorphism effects, smooth animations, touch gestures, and haptic feedback. The responsive design adapts perfectly to your device. Try swiping on messages for options!"

    # Productivity help
    if any(
        word in user_lower
        for word in ["productive", "productivity", "organize", "plan"]
    ):
        analytics = get_analytics()
        return f"📊 **Productivity Insights:**\n• Total tasks created: {analytics['total_tasks_created']}\n• Tasks completed: {analytics['total_tasks_completed']}\n• Active conversations: {analytics['total_conversations']}\n\nI can help you organize your day, manage todos, and boost productivity!"

    # Coding help - Enhanced for specific languages
    if any(
        word in user_lower
        for word in ["java", "teach me java", "learn java", "java help"]
    ):
        return """☕ **Java Programming Tutorial**

**Java Basics:**
```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

**Key Java Concepts:**
• **Classes & Objects:** Everything is an object in Java
• **Variables:** int, String, boolean, double, etc.
• **Methods:** Functions that belong to classes
• **Inheritance:** Extending classes with 'extends'
• **Polymorphism:** One interface, multiple implementations

**Next Steps:**
• Variables and data types
• Control flow (if/else, loops)  
• Object-oriented programming
• Collections (ArrayList, HashMap)

What specific Java topic would you like to learn more about?"""

    elif any(
        word in user_lower
        for word in [
            "code",
            "programming",
            "python",
            "javascript",
            "html",
            "css",
            "coding",
        ]
    ):
        return "💻 I'd love to help with coding! I can assist with:\n• **Java** - OOP, Spring, Android development\n• **Python** - Web apps, data science, automation\n• **JavaScript** - Frontend, Node.js, React\n• **HTML/CSS** - Web design and responsive layouts\n• **And many other languages!**\n\nShare your code or describe what you're building, and I'll provide guidance, debugging help, or code examples."

    # Creative help - Enhanced for specific requests
    if any(
        word in user_lower
        for word in ["magical world", "magic", "fantasy story", "story about"]
    ):
        return """✨ **Magical World Story - "The Crystal Realm"**

*In the land of Aethermoor, where floating islands drift through starlit skies, young Lyra discovered her pendant was more than just a family heirloom...*

**Story Starter:**
"The crystal hummed against her chest as she stepped through the shimmering portal. Before her stretched a world where trees grew upside-down from cloud-banks, and rivers flowed like liquid silver through the air. Dragons the size of hummingbirds danced between her fingers, leaving trails of golden dust.

'Welcome, Dreamweaver,' whispered a voice like wind through ancient forests. 'We've been waiting for you.'"

**World Elements:**
• **Magic System:** Crystal-based powers that respond to emotions
• **Setting:** Floating islands connected by rainbow bridges  
• **Characters:** Lyra (protagonist), wise talking animals, crystal guardians
• **Conflict:** The realm is slowly losing its magic

Would you like me to continue this story or help you create your own magical world?"""

    elif any(
        word in user_lower
        for word in ["creative", "story", "write", "writing", "poem", "article"]
    ):
        return "✨ Creative writing is one of my favorite topics! I can help you:\n• Write stories, poems, or articles\n• Brainstorm ideas\n• Improve existing content\n• Overcome writer's block\n• Create compelling characters and worlds\n\nWhat kind of creative project are you working on?"

    # Analytics request
    if any(
        word in user_lower for word in ["analytics", "stats", "statistics", "progress"]
    ):
        analytics = get_analytics()
        completion_rate = analytics.get("completion_rate", 0)
        return f"📈 **Your Analytics:**\n• Tasks Created: {analytics['total_tasks_created']}\n• Tasks Completed: {analytics['total_tasks_completed']}\n• Completion Rate: {completion_rate:.1f}%\n• Total Conversations: {analytics['total_conversations']}\n• Last Activity: {analytics.get('last_activity', 'N/A')}"

    # Default helpful response
    responses = [
        "🤖 I'm here to help! I can assist with managing todos, coding projects, creative writing, answering questions, and much more. What would you like to work on?",
        "✨ I'm Rex, your AI companion! I can help with productivity, creative tasks, coding, or just have a great conversation. How can I assist you today?",
        "🌟 Thanks for chatting with me! I'm designed to help with a wide range of tasks - from managing your todos to helping with complex projects. What's on your mind?",
        "💡 I'm ready to help! Whether you need assistance with work, creative projects, learning something new, or organizing your tasks, I'm here for you.",
    ]

    import random

    return random.choice(responses)


# Todo management functions
def add_todo_to_storage(task):
    """Add todo to storage"""
    data = load_data(TODO_FILE)
    todo_item = {
        "id": len(data.get("todos", [])) + 1,
        "task": task,
        "completed": False,
        "created_at": datetime.now().isoformat(),
    }
    data.setdefault("todos", []).append(todo_item)
    save_data(TODO_FILE, data)

    # Update analytics
    update_analytics("task_created")


def get_todos():
    """Get all todos"""
    data = load_data(TODO_FILE)
    return data.get("todos", [])


def get_todo_count():
    """Get todo count"""
    return len(get_todos())


def update_analytics(action):
    """Update analytics"""
    data = load_data(STORAGE_FILE)
    analytics = data.get("analytics", {})

    if action == "task_created":
        analytics["total_tasks_created"] = analytics.get("total_tasks_created", 0) + 1
    elif action == "task_completed":
        analytics["total_tasks_completed"] = (
            analytics.get("total_tasks_completed", 0) + 1
        )
    elif action == "conversation":
        analytics["total_conversations"] = analytics.get("total_conversations", 0) + 1

    # Calculate completion rate
    created = analytics.get("total_tasks_created", 0)
    completed = analytics.get("total_tasks_completed", 0)
    analytics["completion_rate"] = (completed / created * 100) if created > 0 else 0
    analytics["last_activity"] = datetime.now().isoformat()

    data["analytics"] = analytics
    save_data(STORAGE_FILE, data)


def get_analytics():
    """Get analytics data"""
    data = load_data(STORAGE_FILE)
    return data.get("analytics", {})


# Routes
@app.route("/")
def index():
    """Serve the mobile-optimized template"""
    try:
        return render_template("index_mobile_optimized.html")
    except Exception as e:
        print(f"Error rendering mobile-optimized index: {e}")
        try:
            return render_template("index.html")
        except:
            return "Error loading the application", 500


@app.route("/desktop")
def desktop():
    """Serve the original desktop template"""
    try:
        return render_template("index.html")
    except Exception as e:
        print(f"Error rendering desktop index: {e}")
        return "Error loading the application", 500


@app.route("/api/chat", methods=["POST"])
def chat():
    """Handle chat requests with full functionality"""
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # Load chat history
        storage_data = load_data(STORAGE_FILE)
        chat_history = storage_data.get("conversation_history", [])

        # Add user message to history
        chat_history.append(
            {
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Get AI response
        ai_response = get_ai_response(user_message)

        # Add AI response to history
        chat_history.append(
            {
                "role": "assistant",
                "content": ai_response,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Update storage
        storage_data["conversation_history"] = chat_history
        save_data(STORAGE_FILE, storage_data)

        # Update analytics
        update_analytics("conversation")

        return jsonify({"response": ai_response, "status": "success"})

    except Exception as e:
        print(f"❌ Chat error: {e}")
        traceback.print_exc()
        return (
            jsonify(
                {"error": f"Failed to process message: {str(e)}", "status": "error"}
            ),
            500,
        )


@app.route("/prompt", methods=["POST"])
def prompt_fallback():
    """Legacy endpoint fallback - redirects to /api/chat"""
    try:
        data = request.get_json()
        user_message = data.get("prompt", "").strip()

        if not user_message:
            return jsonify({"error": "Prompt is required"}), 400

        # Load chat history
        storage_data = load_data(STORAGE_FILE)
        chat_history = storage_data.get("conversation_history", [])

        # Add user message to history
        chat_history.append(
            {
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Get AI response
        ai_response = get_ai_response(user_message)

        # Add AI response to history
        chat_history.append(
            {
                "role": "assistant",
                "content": ai_response,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Update storage
        storage_data["conversation_history"] = chat_history
        save_data(STORAGE_FILE, storage_data)

        # Update analytics
        update_analytics("conversation")

        return jsonify({"response": ai_response, "status": "success"})

    except Exception as e:
        print(f"❌ Prompt error: {e}")
        traceback.print_exc()
        return (
            jsonify(
                {"error": f"Failed to process prompt: {str(e)}", "status": "error"}
            ),
            500,
        )


@app.route("/api/history")
def get_history():
    """Get chat history"""
    try:
        data = load_data(STORAGE_FILE)
        return jsonify(
            {"history": data.get("conversation_history", []), "status": "success"}
        )
    except Exception as e:
        print(f"Error getting history: {e}")
        return jsonify({"error": "Failed to load history"}), 500


@app.route("/api/stats")
def get_stats():
    """Get statistics for the dashboard"""
    try:
        analytics = get_analytics()
        todos = get_todos()
        active_todos = len([t for t in todos if not t.get("completed", False)])

        return jsonify(
            {
                "messageCount": analytics.get("total_conversations", 0),
                "sessionTime": "Active",
                "todoCount": active_todos,
                "completedTasks": analytics.get("total_tasks_completed", 0),
                "totalTasks": analytics.get("total_tasks_created", 0),
                "status": "success",
            }
        )
    except Exception as e:
        print(f"Error getting stats: {e}")
        return jsonify({"error": "Failed to load stats"}), 500


@app.route("/api/todos", methods=["GET"])
def api_get_todos():
    """Get todos via API"""
    try:
        todos = get_todos()
        return jsonify({"todos": todos, "count": len(todos), "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/todos", methods=["POST"])
def api_add_todo():
    """Add todo via API"""
    try:
        data = request.get_json()
        task = data.get("task", "").strip()

        if not task:
            return jsonify({"error": "Task is required"}), 400

        add_todo_to_storage(task)
        return jsonify({"message": "Todo added successfully", "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/clear", methods=["POST"])
def clear_history():
    """Clear chat history"""
    try:
        data = load_data(STORAGE_FILE)
        data["conversation_history"] = []
        save_data(STORAGE_FILE, data)
        return jsonify({"status": "success", "message": "Chat history cleared"})
    except Exception as e:
        print(f"Error clearing history: {e}")
        return jsonify({"error": "Failed to clear history"}), 500


# Static file serving
@app.route("/manifest.json")
def manifest():
    """Serve manifest file"""
    return send_from_directory(".", "manifest.json")


@app.route("/sw.js")
def service_worker():
    """Serve service worker"""
    return send_from_directory("static", "sw.js")


@app.route("/favicon.ico")
def favicon():
    """Serve favicon"""
    return send_from_directory("static", "favicon.ico")


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    # Initialize storage
    init_storage()

    print("🚀 Starting Rex AI Assistant - Full Featured Mobile App")
    print("=" * 60)
    print("📱 Beautiful Mobile Interface + Full AI Functionality!")
    print()
    print("🌟 Core Features:")
    print("  ✅ Real AI conversations (OpenRouter/DeepSeek)")
    print("  ✅ Todo list management")
    print("  ✅ Chat history persistence")
    print("  ✅ Analytics and insights")
    print("  ✅ Mobile-optimized UI with animations")
    print("  ✅ Offline PWA capabilities")
    print("  ✅ Touch gestures and haptic feedback")
    print()
    print("🌐 Access Points:")
    print("  • Mobile (default): http://localhost:5000")
    print("  • Desktop version: http://localhost:5000/desktop")
    print()
    print("🔧 API Endpoints:")
    print("  • Chat: POST /api/chat")
    print("  • Stats: GET /api/stats")
    print("  • Todos: GET/POST /api/todos")
    print("  • History: GET /api/history")

    try:
        port = int(os.environ.get("PORT", 5000))
        debug = os.environ.get("FLASK_ENV") == "development"

        app.run(host="0.0.0.0", port=port, debug=debug, threaded=True)
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        traceback.print_exc()
