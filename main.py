import json
import redis
import os
from flask import Flask, render_template, request, jsonify
from app.agent import agent_executor
from langchain_core.messages import HumanMessage, AIMessage

app = Flask(__name__)

# Connect to Redis
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.from_url(redis_url)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prompt', methods=['POST'])
def prompt():
    user_input = request.json['prompt']
    
    # Load chat history from Redis
    chat_history_json = r.get("chat_history")
    chat_history = []
    if chat_history_json:
        chat_history_list = json.loads(chat_history_json)
        chat_history = [HumanMessage(**msg) if msg['type'] == 'human' else AIMessage(**msg) for msg in chat_history_list]

    response = agent_executor.invoke({
        "input": user_input,
        "chat_history": chat_history
    })

    # Save chat history to Redis
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response["output"]))
    chat_history_list = [msg.dict() for msg in chat_history]
    r.set("chat_history", json.dumps(chat_history_list))

    return jsonify({'response': response['output']})

if __name__ == '__main__':
    app.run()