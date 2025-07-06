# Snello - Your Personal AI Assistant

Snello is a web-based chatbot that helps you manage your to-do list. It's built with Python, Flask, LangChain, and Google's Gemini API. Snello is designed to be a simple, yet powerful, example of an AI agent that can understand and respond to your requests in a conversational way.

## Architecture

The application follows a simple agentic architecture based on the LangChain library. Here's a breakdown of the components:

- **main.py**: The entry point of the application. It runs a Flask web server that serves the web interface and handles user prompts.
- **app/agent.py**: This is the core of the agent. It defines the LLM, the tools, the prompt, and the agent executor.
- **app/tools.py**: This module contains the tools that the agent can use to interact with the outside world. In this case, it has tools for adding, removing, and listing to-do items.
- **templates/index.html**: The HTML file for the web interface.
- **static/style.css**: The CSS file for styling the web interface.
- **static/script.js**: The JavaScript file for handling user interactions in the web interface.
- **.env**: This file stores the `GOOGLE_API_KEY` required to use the Gemini API.
- **todolist.json**: This file is used to persist the to-do list.

The agent uses a tool-calling approach, where the LLM can decide to call one of the provided tools to fulfill a user's request. The `AgentExecutor` manages the flow of the conversation, passing the user's input to the agent and executing any tool calls that the agent decides to make.

## Memory

Snello persists both conversation history and the to-do list in a single JSON file named `storage.json`. This ensures that your conversations and to-do items are saved even after the application is closed.

## Tools

The agent has access to the following tools, which interact with the `storage.json` file:

- **`add_todo(todo: str)`**: Adds a new item to the to-do list.
- **`remove_todo(todo_index: int)`**: Removes an item from the to-do list by its index.
- **`list_todos()`**: Lists all items currently in the to-do list.

These tools are defined in `app/tools.py` and are decorated with the `@tool` decorator from LangChain. This decorator makes the functions available to the agent, and the docstrings of the functions are used by the LLM to determine when and how to use them.

## Setup and Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/jigs1188/ChatBot
    cd snello
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your API key:**
    -   Create a file named `.env` in the root of the project.
    -   Add the following line to the `.env` file, replacing `"YOUR_API_KEY_HERE"` with your actual Google API key:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```

4.  **Run the application:**
    ```bash
    python main.py
    ```

5.  **Open the web interface:**
    Open your web browser and go to `http://127.0.0.1:5000`.

## Limitations and Future Improvements

-   **Error Handling**: The error handling is basic. More robust error handling could be added to handle cases like invalid API keys or network issues.
-   **More Tools**: The agent could be extended with more tools, such as the ability to set reminders or integrate with other applications.