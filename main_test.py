import json
import os
from flask import Flask, render_template, request, jsonify
from pathlib import Path

app = Flask(__name__)

# Simple test route
@app.route('/')
def index():
    return render_template('simple.html')

@app.route('/simple')
def simple():
    return render_template('simple.html')

@app.route('/test-prompt', methods=['POST'])
def test_prompt():
    """Simple test endpoint without AI"""
    try:
        user_input = request.json.get('prompt', '').strip()
        print(f"📩 Test prompt received: {user_input}")
        
        if not user_input:
            return jsonify({'error': 'Empty prompt provided'}), 400
            
        # Simple echo response for testing
        response = f"Echo: {user_input} (This is a test response without AI)"
        
        return jsonify({'response': response})
    
    except Exception as e:
        print(f"❌ Error in test prompt: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Test server running'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Starting test server...")
    app.run(host='0.0.0.0', port=port, debug=True)
