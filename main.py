from flask import Flask, render_template, request, jsonify
from app.agent import agent_executor
from langchain_core.messages import HumanMessage, AIMessage

app = Flask(__name__)

# In-memory store for conversation history
chat_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prompt', methods=['POST'])
def prompt():
    user_input = request.json['prompt']
    
    # Invoke the agent with the user input and chat history
    response = agent_executor.invoke({
        "input": user_input,
        "chat_history": chat_history
    })

    # Append the conversation to history
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response["output"]))

    return jsonify({'response': response['output']})

if __name__ == '__main__':
    app.run(debug=True)