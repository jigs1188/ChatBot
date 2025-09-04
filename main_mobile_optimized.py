import json
import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
import traceback

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Import the agent system
from app.agent import get_agent_executor

app = Flask(__name__)

# File-based storage for chat history
STORAGE_FILE = Path(__file__).parent / "storage.json"


def load_chat_history():
    """Load chat history from storage file"""
    try:
        if STORAGE_FILE.exists():
            with open(STORAGE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("conversation_history", [])
        return []
    except Exception as e:
        print(f"Error loading chat history: {e}")
        return []


def save_chat_history(chat_history):
    """Save chat history to storage file"""
    try:
        # Load existing data
        data = {"conversation_history": [], "todo_list": [], "user_name": None}
        if STORAGE_FILE.exists():
            with open(STORAGE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

        # Update conversation history
        data["conversation_history"] = chat_history

        # Save back to file
        with open(STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving chat history: {e}")


def get_ai_response(user_input):
    """Get response from AI agent with tools"""
    try:
        print(f"🤖 Getting AI response for: {user_input[:100]}...")

        # Get the agent executor
        agent_executor = get_agent_executor()

        # Run the agent
        result = agent_executor.invoke({"input": user_input})
        response = result.get("output", "I'm sorry, I couldn't process your request.")

        print(f"✅ AI response generated successfully")
        return response

    except Exception as e:
        print(f"❌ Error getting AI response: {e}")
        traceback.print_exc()
        return f"I apologize, but I encountered an error while processing your request: {str(e)}"


@app.route("/")
def index():
    """Serve the mobile-optimized template"""
    try:
        return render_template("index_mobile_optimized.html")
    except Exception as e:
        print(f"Error rendering mobile-optimized index: {e}")
        # Fallback to original template
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


@app.route("/simple")
def simple():
    """Simple version without complex loading"""
    try:
        return render_template("simple.html")
    except Exception as e:
        print(f"Error rendering simple page: {e}")
        return "Error loading the simple application", 500


@app.route("/api/chat", methods=["POST"])
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # Load chat history
        chat_history = load_chat_history()

        # Add user message to history
        chat_history.append(
            {
                "role": "user",
                "content": user_message,
                "timestamp": str(Path().resolve()),
            }
        )

        # Get AI response
        ai_response = get_ai_response(user_message)

        # Add AI response to history
        chat_history.append(
            {
                "role": "assistant",
                "content": ai_response,
                "timestamp": str(Path().resolve()),
            }
        )

        # Save updated history
        save_chat_history(chat_history)

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


@app.route("/api/history")
def get_history():
    """Get chat history"""
    try:
        chat_history = load_chat_history()
        return jsonify({"history": chat_history, "status": "success"})
    except Exception as e:
        print(f"Error getting history: {e}")
        return jsonify({"error": "Failed to load history"}), 500


@app.route("/api/clear", methods=["POST"])
def clear_history():
    """Clear chat history"""
    try:
        save_chat_history([])
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
    try:
        print("🚀 Starting Mobile-Optimized Rex AI Assistant...")
        print("📱 Beautiful mobile interface ready!")
        print("🌐 Access at: http://localhost:5000")
        print("💻 Desktop version: http://localhost:5000/desktop")
        print("📱 Mobile-optimized: http://localhost:5000 (default)")

        # Check if running on mobile-friendly port
        port = int(os.environ.get("PORT", 5000))
        debug = os.environ.get("FLASK_ENV") == "development"

        app.run(host="0.0.0.0", port=port, debug=debug, threaded=True)
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        traceback.print_exc()
