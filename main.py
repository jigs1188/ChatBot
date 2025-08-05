import json
from flask import Flask, render_template, request, jsonify
from app.agent import agent_executor
from langchain_core.messages import HumanMessage, AIMessage

app = Flask(__name__)

def load_storage():
    try:
        with open('storage.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'conversation_history': [], 'todo_list': []}

def save_storage(data):
    with open('storage.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prompt', methods=['POST'])
def prompt():
    user_input = request.json['prompt']
    storage = load_storage()
    chat_history = [HumanMessage(**msg) if msg['type'] == 'human' else AIMessage(**msg) for msg in storage['conversation_history']]

    response = agent_executor.invoke({
        "input": user_input,
        "chat_history": chat_history
    })

    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response["output"]))
    storage['conversation_history'] = [msg.dict() for msg in chat_history]
    save_storage(storage)

    return jsonify({'response': response['output']})

if __name__ == '__main__':
    app.run()