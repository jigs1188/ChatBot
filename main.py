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

def get_ai_response(user_input):
    """Get response from AI agent with tools"""
    try:
        # Get the agent executor
        agent_executor = get_agent_executor()
        
        if not agent_executor:
            return "Please configure your API key to enable AI responses."
        
        # Use the agent to process the input
        result = agent_executor.invoke({"input": user_input})
        return result.get("output", "Sorry, I couldn't process that request.")
        
    except Exception as e:
        print(f"Error calling AI agent: {e}")
        return f"Sorry, I'm having trouble connecting right now. Please try again later."

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

        # Get response from AI agent with tools
        print("🤖 Calling AI agent...")
        ai_response = get_ai_response(user_input)
        print(f"✅ AI response received: {ai_response[:100]}...")

        # Save updated chat history to file
        print("💾 Saving chat history...")
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        chat_history.append({"role": "user", "content": user_input, "timestamp": timestamp})
        chat_history.append({"role": "assistant", "content": ai_response, "timestamp": timestamp})
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
    return jsonify({'status': 'healthy', 'message': 'Rex is running'}), 200

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
        google_key = os.getenv('GOOGLE_API_KEY')
        openrouter_key = os.getenv('OPENROUTER_API_KEY')
        api_configured = bool(google_key or openrouter_key)
        
        return jsonify({
            'status': 'OK',
            'message': 'All systems operational',
            'version': '2.0.0',
            'features': ['AI Assistant', 'Todo Management', 'Mobile-First', 'PWA'],
            'api_configured': api_configured,
            'endpoints': ['/prompt', '/api/debug', '/health']
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/handle-file', methods=['POST'])
def handle_file():
    """Handle file uploads for PWA"""
    return jsonify({'message': 'File handling not implemented yet'}), 200

@app.route('/share', methods=['GET'])
def handle_share():
    """Handle share target for PWA"""
    title = request.args.get('title', '')
    text = request.args.get('text', '')
    url = request.args.get('url', '')
    return render_template('index.html', shared_content={'title': title, 'text': text, 'url': url})

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
    
    print("🚀 Starting Rex AI Assistant...")
    google_key = os.getenv('GOOGLE_API_KEY')
    openrouter_key = os.getenv('OPENROUTER_API_KEY')
    api_configured = bool(google_key or openrouter_key)
    print(f"✅ API Key: {'✅ Configured' if api_configured else '❌ Missing'}")
    print(f"🌐 Server starting on http://127.0.0.1:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
