#!/usr/bin/env python3
import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Rex AI Server Test - OK"

@app.route('/api/stats')
def get_stats():
    return jsonify({
        "messageCount": 5,
        "sessionTime": "Active",
        "todoCount": 2,
        "completedTasks": 3,
        "totalTasks": 5,
        "status": "success"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    return jsonify({
        "response": "Hello! I'm working correctly now.",
        "status": "success"
    })

if __name__ == '__main__':
    print("🚀 Testing Rex AI Server...")
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    app.run(host=host, port=port, debug=debug)
