# Snello - Your Personal AI Assistant

Snello is a command-line chatbot that helps you manage your to-do list. It's built with Python, LangChain, and Google's Gemini API. Snello is designed to be a simple, yet powerful, example of an AI agent that can understand and respond to your requests in a conversational way.

## Architecture

The application follows a simple agentic architecture based on the LangChain library. Here's a breakdown of the components:

- **main.py**: The entry point of the application. It handles the command-line interface (CLI), manages the conversation history, and invokes the agent.
- **app/agent.py**: This is the core of the agent. It defines the LLM, the tools, the prompt, and the agent executor.
- **app/tools.py**: This module contains the tools that the agent can use to interact with the outside world. In this case, it has tools for adding, removing, and listing to-do items.
- **.env**: This file stores the `GOOGLE_API_KEY` required to use the Gemini API.
- **todolist.json**: This file is used to persist the to-do list.

The agent uses a tool-calling approach, where the LLM can decide to call one of the provided tools to fulfill a user's request. The `AgentExecutor` manages the flow of the conversation, passing the user's input to the agent and executing any tool calls that the agent decides to make.

## Memory

Snello has two types of memory:

1.  **Conversation History**: The conversation history is stored in-memory as a list of messages. This allows the agent to remember previous turns in the conversation and respond in a more context-aware way. The history is passed to the agent with each new user input.

2.  **To-Do List**: The to-do list is persisted in a JSON file named `todolist.json`. The `app/tools.py` module contains functions for reading from and writing to this file, ensuring that your to-do list is saved even after you close the application.

## Tools

The agent has access to the following tools:

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

## Example Prompts

Here are some examples of how you can interact with Snello:

-   `Hello, my name is [Your Name]`
-   `Add "buy groceries" to my to-do list`
-   `What's on my to-do list?`
-   `Add "finish the report" to my list`
-   `Can you remove "buy groceries" from my list?`
-   `Show me my to-dos`

## Limitations and Future Improvements

-   **In-Memory Chat History**: The conversation history is currently stored in-memory, which means it will be lost when the application is closed. A future improvement would be to persist the chat history to a file or a database.
-   **Error Handling**: The error handling is basic. More robust error handling could be added to handle cases like invalid API keys or network issues.
-   **Web Interface**: The current interface is a command-line interface. A web interface could be built to provide a more user-friendly experience.
-   **More Tools**: The agent could be extended with more tools, such as the ability to set reminders or integrate with other applications.
