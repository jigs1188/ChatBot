import json
import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
import traceback

app = Flask(__name__)

# Simple chat responses for demo
DEMO_RESPONSES = [
    "🎉 Welcome to Rex AI! I'm your mobile-optimized AI companion. How can I help you today?",
    "✨ I'm here to assist with conversations, creative tasks, coding help, and much more!",
    "🚀 Thanks for trying the beautiful mobile interface! What would you like to explore?",
    "🤖 I'm Rex AI - your intelligent assistant optimized for mobile devices. Ask me anything!",
    "💡 I can help with writing, analysis, problem-solving, and creative projects. What interests you?",
    "🌟 The mobile experience has been completely redesigned for touch interactions. How do you like it?",
    "📱 Swipe gestures, haptic feedback, and beautiful animations make chatting a joy!",
    "🎨 I can help with creative writing, code development, data analysis, and learning new topics."
]

@app.route('/')
def index():
    """Serve the mobile-optimized template"""
    try:
        return render_template('index_mobile_optimized.html')
    except Exception as e:
        print(f"Error rendering mobile-optimized index: {e}")
        # Fallback to original template
        try:
            return render_template('index.html')
        except:
            return "Error loading the application", 500

@app.route('/desktop')
def desktop():
    """Serve the original desktop template"""
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering desktop index: {e}")
        return "Error loading the application", 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests with demo responses"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Simple demo response logic
        import random
        
        if 'hello' in user_message.lower() or 'hi' in user_message.lower():
            response = "👋 Hello! Welcome to the beautiful mobile-optimized Rex AI! I'm excited to chat with you."
        elif 'mobile' in user_message.lower() or 'responsive' in user_message.lower():
            response = "📱 Yes! This interface has been completely redesigned for mobile devices with beautiful animations, touch gestures, and haptic feedback. Try swiping on messages!"
        elif 'beautiful' in user_message.lower() or 'ui' in user_message.lower() or 'design' in user_message.lower():
            response = "✨ Thank you! The new mobile interface features glassmorphism effects, gradient animations, smooth transitions, and interactive micro-animations. Every element is optimized for touch!"
        elif 'help' in user_message.lower():
            response = "🤖 I'm here to help! Try the quick actions in the sidebar, use voice input, or just type naturally. The interface adapts to your mobile device perfectly!"
        elif 'code' in user_message.lower() or 'programming' in user_message.lower():
            response = "💻 I'd love to help with coding! The mobile interface makes it easy to discuss code, get suggestions, and learn programming concepts on your phone or tablet."
        elif 'creative' in user_message.lower() or 'story' in user_message.lower():
            response = "🎨 Creative tasks are my specialty! The mobile interface makes brainstorming and creative writing feel natural with its intuitive design and smooth interactions."
        else:
            response = random.choice(DEMO_RESPONSES)
        
        return jsonify({
            "response": response,
            "status": "success"
        })
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        traceback.print_exc()
        return jsonify({
            "error": f"Failed to process message: {str(e)}",
            "status": "error"
        }), 500

@app.route('/api/history')
def get_history():
    """Get demo chat history"""
    return jsonify({
        "history": [],
        "status": "success"
    })

@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear chat history"""
    return jsonify({"status": "success", "message": "Chat history cleared"})

# Static file serving
@app.route('/manifest.json')
def manifest():
    """Serve manifest file"""
    return send_from_directory('.', 'manifest.json')

@app.route('/sw.js')
def service_worker():
    """Serve service worker"""
    return send_from_directory('static', 'sw.js')

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory('static', 'favicon.ico')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    try:
        print("🚀 Starting Beautiful Mobile-Optimized Rex AI Assistant...")
        print("📱 Stunning mobile interface with glassmorphism and animations!")
        print("🌟 Features: Touch gestures, haptic feedback, smooth transitions")
        print("🌐 Access at: http://localhost:5000")
        print("💻 Desktop version: http://localhost:5000/desktop")
        print("📱 Mobile-optimized: http://localhost:5000 (default)")
        print()
        print("✨ Mobile UI Features:")
        print("  • Beautiful glassmorphism effects")
        print("  • Smooth animations and transitions")
        print("  • Touch-optimized interactions")
        print("  • Swipe gestures for navigation")
        print("  • Haptic feedback on touch")
        print("  • Responsive design for all screen sizes")
        print("  • Enhanced PWA capabilities")
        
        # Check if running on mobile-friendly port
        port = int(os.environ.get('PORT', 5000))
        debug = os.environ.get('FLASK_ENV') == 'development'
        
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug,
            threaded=True
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        traceback.print_exc()
