#!/usr/bin/env python3
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "Rex AI Server Test - OK"


@app.route("/api/stats")
def get_stats():
    return jsonify(
        {
            "messageCount": 5,
            "sessionTime": "Active",
            "todoCount": 2,
            "completedTasks": 3,
            "totalTasks": 5,
            "status": "success",
        }
    )


@app.route("/api/chat", methods=["POST"])
def chat():
    return jsonify(
        {"response": "Hello! I'm working correctly now.", "status": "success"}
    )


if __name__ == "__main__":
    print("🚀 Testing Rex AI Server...")
    app.run(host="0.0.0.0", port=5000, debug=True)
