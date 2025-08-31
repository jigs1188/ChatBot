import json
import os
import requests
import traceback
from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# File-based storage for chat history
STORAGE_FILE = Path(__file__).parent / "storage.json"

def load_chat_history():
    """Load chat history from storage file"""
    try:
        if STORAGE_FILE.exists():
            with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
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
            with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        # Update conversation history
        data["conversation_history"] = chat_history
        
        # Save back to file
        with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving chat history: {e}")

def get_deepseek_response(user_input, chat_history=[]):
    """Get response from DeepSeek via OpenRouter"""
    try:
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if not openrouter_key:
            return "❌ Please configure your OpenRouter API key to enable AI responses."
        
        # Build conversation history for context
        messages = [
            {
                "role": "system",
                "content": """You are Snello AI, a helpful and friendly personal assistant. You help users with:
                
🎯 Task Management: Add, remove, complete, and organize todos
📊 Analytics: Provide insights about productivity and habits  
💡 Creative Help: Brainstorming, writing, and problem-solving
🔍 Information: Answer questions and provide useful information
📅 Planning: Help organize schedules and daily activities

Keep responses concise, helpful, and engaging. Use emojis appropriately to make interactions friendly."""
            }
        ]
        
        # Add recent chat history for context (last 10 messages)
        recent_history = chat_history[-10:] if len(chat_history) > 10 else chat_history
        for msg in recent_history:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        headers = {
            "Authorization": f"Bearer {openrouter_key}",
            "HTTP-Referer": "https://snello-ai.com",
            "X-Title": "Snello AI Assistant",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek/deepseek-chat",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1500,
            "stream": False
        }
        
        print(f"🔗 Calling DeepSeek API with {len(messages)} messages...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"📡 API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            print(f"✅ DeepSeek Response: {ai_response[:100]}...")
            return ai_response
        else:
            error_text = response.text
            print(f"❌ OpenRouter API error: {response.status_code} - {error_text}")
            return f"Sorry, I encountered an API error (Status: {response.status_code}). Please try again."
            
    except requests.exceptions.Timeout:
        return "⏰ The request timed out. Please try again with a shorter message."
    except requests.exceptions.ConnectionError:
        return "🌐 Connection error. Please check your internet connection and try again."
    except Exception as e:
        print(f"❌ Error calling DeepSeek API: {e}")
        return f"🔧 Sorry, I'm having trouble connecting right now. Please try again later."

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering index: {e}")
        return "Error loading the application", 500

@app.route('/simple')
def simple():
    """Simple version without complex loading"""
    try:
        return render_template('simple.html')
    except Exception as e:
        print(f"Error rendering simple page: {e}")
        return "Error loading simple page", 500

@app.route('/debug')
def debug_page():
    """Debug page for testing"""
    try:
        return render_template('debug.html')
    except Exception as e:
        print(f"Error rendering debug page: {e}")
        return "Error loading debug page", 500

@app.route('/prompt', methods=['POST'])
def prompt():
    try:
        print(f"📩 Received prompt request")
        user_input = request.json.get('prompt', '').strip()
        print(f"📝 User input: {user_input}")
        
        if not user_input:
            return jsonify({'error': 'Empty prompt provided'}), 400
        
        # Load chat history from file
        print("📚 Loading chat history...")
        chat_history = load_chat_history()
        print(f"💾 Loaded {len(chat_history)} previous messages")

        # Get response from DeepSeek directly
        print("🤖 Calling DeepSeek API...")
        ai_response = get_deepseek_response(user_input, chat_history)
        print(f"✅ DeepSeek response received: {ai_response[:100]}...")

        # Save updated chat history to file
        print("💾 Saving chat history...")
        chat_history.append({"role": "user", "content": user_input, "timestamp": "now"})
        chat_history.append({"role": "assistant", "content": ai_response, "timestamp": "now"})
        save_chat_history(chat_history)
        print("✅ Chat history saved")

        return jsonify({'response': ai_response})
    
    except Exception as e:
        print(f"❌ Error processing prompt: {e}")
        print(f"🔍 Full traceback: {traceback.format_exc()}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Snello is running'}), 200

@app.route('/manifest.json')
def manifest():
    """Serve PWA manifest"""
    return send_from_directory('static', 'manifest.json', mimetype='application/json')

@app.route('/sw.js')
def service_worker():
    """Serve service worker"""
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

@app.route('/api/debug', methods=['GET'])
def debug_info():
    """Debug endpoint to check app status"""
    try:
        return jsonify({
            'status': 'OK',
            'message': 'All systems operational',
            'version': '1.1.0',
            'features': ['DeepSeek V3.1', 'Mobile-First', 'PWA'],
            'api_configured': bool(os.getenv("OPENROUTER_API_KEY")),
            'endpoints': ['/prompt', '/api/debug', '/health']
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get application statistics"""
    try:
        chat_history = load_chat_history()
        return jsonify({
            'total_messages': len(chat_history),
            'total_todos': 0,  # Simplified for now
            'user_name': 'User',
            'uptime': 'Online'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Check if running in production
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print("🚀 Starting Snello AI Assistant...")
    print(f"✅ DeepSeek API Key: {'✅ Configured' if os.getenv('OPENROUTER_API_KEY') else '❌ Missing'}")
    print(f"🌐 Server starting on http://127.0.0.1:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
