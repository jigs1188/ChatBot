import json
import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from datetime import datetime

app = Flask(__name__)

# Simple in-memory storage for demos (resets on each deploy)
todo_list = []
chat_history = []
user_name = None

def get_ai_response(user_input):
    """Get AI response using OpenRouter API directly"""
    try:
        import requests
        
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return "❌ Please configure your OPENROUTER_API_KEY environment variable in Vercel dashboard."
        
        # Simple todo management
        user_lower = user_input.lower()
        
        # Handle todo commands directly
        if any(word in user_lower for word in ["add", "create"]) and any(word in user_lower for word in ["todo", "task", "list"]):
            # Extract task from input
            task = user_input
            for word in ["add", "create", "to", "todo", "task", "list", "my"]:
                task = task.replace(word, "").replace(word.capitalize(), "")
            task = task.strip(' "\'.,!')
            
            if task:
                todo_list.append({
                    "task": task,
                    "completed": False,
                    "created": datetime.now().isoformat()
                })
                return f"✅ Added '{task}' to your todo list! You now have {len(todo_list)} tasks."
            else:
                return "❓ What task would you like to add? Try: 'Add buy groceries'"
        
        elif any(word in user_lower for word in ["show", "list", "display", "what"]):
            if not todo_list:
                return "📝 Your todo list is empty! Try adding a task: 'Add buy milk'"
            
            result = "📋 **Your Todo List:**\n\n"
            for i, item in enumerate(todo_list, 1):
                status = "✅" if item["completed"] else "⭕"
                result += f"{i}. {status} {item['task']}\n"
            
            completed = sum(1 for item in todo_list if item["completed"])
            result += f"\n📊 Progress: {completed}/{len(todo_list)} completed"
            return result
        
        elif any(word in user_lower for word in ["complete", "done", "finish"]):
            if not todo_list:
                return "📝 No tasks to complete! Add some tasks first."
            
            # Find first incomplete task
            for item in todo_list:
                if not item["completed"]:
                    item["completed"] = True
                    return f"🎉 Marked '{item['task']}' as completed! Great job!"
            
            return "🎉 All tasks are already completed! You're doing great!"
        
        elif any(word in user_lower for word in ["clear", "delete", "remove"]):
            count = len(todo_list)
            todo_list.clear()
            return f"🗑️ Cleared {count} tasks from your list. Fresh start!"
        
        # For other inputs, use AI
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = """You are Rex AI, a friendly personal assistant that helps with todo list management. 

You can help users:
- Add tasks: "add buy milk"
- Show tasks: "show my list"  
- Complete tasks: "complete task"
- Clear all: "clear my list"

Keep responses helpful, encouraging, and concise. Use emojis to make it friendly."""
        
        data = {
            "model": "deepseek/deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.7,
            "max_tokens": 300
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions", 
            headers=headers, 
            json=data, 
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return "I can help you manage your todos! Try: 'add buy groceries' or 'show my list'"
            
    except Exception as e:
        return f"Hello! I'm Rex AI. I can help you manage your todo list. Try saying: 'add buy milk' or 'show my tasks'"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prompt', methods=['POST'])
def prompt():
    try:
        user_input = request.json.get('prompt', '').strip()
        if not user_input:
            return jsonify({'error': 'Please enter a message'}), 400
        
        # Get AI response
        ai_response = get_ai_response(user_input)
        
        # Store conversation in memory
        timestamp = datetime.now().isoformat()
        chat_history.append({"role": "user", "content": user_input, "timestamp": timestamp})
        chat_history.append({"role": "assistant", "content": ai_response, "timestamp": timestamp})
        
        # Keep only last 20 messages to prevent memory issues
        if len(chat_history) > 20:
            chat_history[:] = chat_history[-20:]
        
        return jsonify({'response': ai_response})
    
    except Exception as e:
        error_msg = "I'm having trouble right now. Try a simple command like 'add task' or 'show list'"
        return jsonify({'response': error_msg})

@app.route('/manifest.json')
def serve_manifest():
    """Serve PWA manifest directly"""
    manifest_data = {
        "id": "rex-ai-assistant-app",
        "name": "Rex AI Assistant",
        "short_name": "Rex",
        "description": "Your intelligent AI assistant for productivity and task management",
        "start_url": "/",
        "display": "standalone",
        "display_override": ["window-controls-overlay", "standalone"],
        "background_color": "#0f172a",
        "theme_color": "#6366f1",
        "orientation": "portrait-primary",
        "scope": "/",
        "lang": "en-US",
        "dir": "ltr",
        "categories": ["productivity", "utilities", "business"],
        "iarc_rating_id": "e84b072d-71de-3dae-a8ea-1234567890ab",
        "launch_handler": {
            "client_mode": "focus-existing"
        },
        "icons": [
            {
                "src": "/static/icon-72.png",
                "sizes": "72x72",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "/static/icon-96.png",
                "sizes": "96x96",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "/static/icon-128.png",
                "sizes": "128x128",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "/static/icon-144.png",
                "sizes": "144x144",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "/static/icon-152.png",
                "sizes": "152x152",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "/static/icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "/static/icon-384.png",
                "sizes": "384x384",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "/static/icon-512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "/static/icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "maskable"
            },
            {
                "src": "/static/icon-512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "maskable"
            }
        ],
        "file_handlers": [
            {
                "action": "/handle-file",
                "accept": {
                    "text/plain": [".txt"],
                    "application/json": [".json"]
                }
            }
        ],
        "share_target": {
            "action": "/share",
            "method": "GET",
            "params": {
                "title": "title",
                "text": "text",
                "url": "url"
            }
        },
        "shortcuts": [
            {
                "name": "Add Todo",
                "short_name": "Add",
                "description": "Quickly add a new todo item",
                "url": "/?action=add-todo",
                "icons": [
                    {
                        "src": "/static/icon-96.png",
                        "sizes": "96x96"
                    }
                ]
            }
        ],
        "edge_side_panel": {
            "preferred_width": 400
        },
        "protocol_handlers": []
    }
    
    response = jsonify(manifest_data)
    response.headers['Content-Type'] = 'application/manifest+json'
    return response

@app.route('/sw.js')
def serve_sw():
    """Serve service worker"""
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve all static files"""
    return send_from_directory('static', filename)

@app.route('/api/debug')
def debug():
    try:
        api_key = os.getenv("OPENROUTER_API_KEY")
        return jsonify({
            'status': 'OK',
            'message': 'Rex AI is running on Vercel',
            'api_configured': bool(api_key),
            'todos_count': len(todo_list),
            'chat_count': len(chat_history),
            'version': '2.0.0'
        })
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
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Vercel entry point
app = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
