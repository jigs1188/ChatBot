# Approach to the Snello SDE Intern Assignment

This document outlines the approach taken to complete the Snello SDE Intern Assignment, including the initial setup, the challenges encountered, and the proposed solutions.

## Initial Setup and Project Structure

The project was initialized with a Flask backend to serve a simple web interface and handle API interactions. The core logic for the AI agent was encapsulated within the `app/` directory, separating concerns for better maintainability.

-   `main.py`: The main Flask application file, responsible for routing, loading/saving conversation history and to-do lists, and interacting with the AI agent.
-   `app/agent.py`: Contains the LangChain agent setup, including the LLM initialization (Gemini 1.5 Flash), tool definitions (`add_todo`, `remove_todo`, `list_todos`), prompt engineering, and the `AgentExecutor`.
-   `app/tools.py`: Defines the custom tools that the AI agent can use to interact with the to-do list functionality.
-   `static/`: Stores static assets like `script.js` (for frontend interactions) and `style.css` (for styling).
-   `templates/`: Contains the `index.html` template for the web interface.
-   `storage.json`: Used for persistent storage of conversation history and the to-do list.
-   `requirements.txt`: Lists all Python dependencies.
-   `.env`: Stores environment variables, specifically the `GOOGLE_API_KEY`.

## AI Agent Design

The AI agent was designed using the LangChain framework, leveraging the `ChatGoogleGenerativeAI` model (Gemini 1.5 Flash).

-   **LLM Selection:** Gemini 1.5 Flash was chosen for its balance of speed and capability, suitable for a conversational agent.
-   **Tooling:** Custom tools (`add_todo`, `remove_todo`, `list_todos`) were implemented to allow the agent to manage a to-do list. This demonstrates the agent's ability to interact with external systems.
-   **Prompt Engineering:** A `ChatPromptTemplate` was used to define the agent's persona ("friendly and helpful assistant named Snello"), provide instructions, and manage chat history. The prompt also includes a mechanism to ask for and use the user's name.
-   **Agent Executor:** The `AgentExecutor` orchestrates the agent's thought process, tool usage, and response generation. `verbose=True` was enabled during development to observe the agent's internal workings.

## Challenge: Google Gemini API Quota Exceeded

During testing and development, a `ResourceExhausted` error was encountered, indicating that the daily free-tier quota for the Google Gemini API had been exceeded.

### Analysis of the Issue

The traceback clearly showed `google.api_core.exceptions.ResourceExhausted` with details about the `generativelanguage.googleapis.com/generate_content_free_tier_requests` quota. This is a common issue with free-tier API usage, especially during active development or with frequent requests.

The current implementation makes an API call to the Gemini model for every user prompt, which is standard for a conversational AI. While `tenacity` (a retry library) was already in place to handle transient errors, it cannot overcome a hard quota limit.

### Proposed Solutions

Since this is a quota limitation rather than a code bug, the solutions primarily involve managing API usage and quotas:

1.  **Upgrade Google Cloud Project:** For sustained usage or production deployment, upgrading the Google Cloud project to a paid tier would remove the free-tier quota limitations.
2.  **Monitor Quota Usage:** Regularly checking the Google Cloud Console's quota page for the Gemini API would provide insights into current usage and reset times.
3.  **Optimize API Calls (if applicable):** While not directly applicable to a real-time conversational agent, for other types of applications, strategies like caching common responses or batching requests could reduce API calls. However, for this assignment, each user interaction necessitates an LLM call.
4.  **Alternative API Keys/Models:** If available, using a different API key or a model with higher quotas could be a temporary workaround.

## Conclusion

The project demonstrates a functional AI agent capable of managing a to-do list through natural language interaction. The primary challenge encountered was an external API quota limitation, which is a common operational consideration for AI-powered applications. Addressing this would involve quota management strategies rather than code changes to the core logic.
