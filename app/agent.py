
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from app.tools import add_todo, remove_todo, list_todos, save_user_name

# --- 1. Load the LLM ---
# We are using the ChatGoogleGenerativeAI class to interact with the Gemini API.
# The model is set to "gemini-1.5-flash" for a balance of speed and capability.
# `convert_system_message_to_human=True` is a compatibility setting for some models.
# The GOOGLE_API_KEY is loaded from the .env file automatically by `load_dotenv()`.
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", convert_system_message_to_human=True)

# --- 2. Define the Tools ---
# The tools are the functions the agent can call to interact with the outside world.
# In this case, we have tools for managing a to-do list.
tools = [add_todo, remove_todo, list_todos, save_user_name]

# --- 3. Create the Prompt ---
# The prompt is the set of instructions that guides the agent's behavior.
# It includes a system message, placeholders for chat history and user input,
# and a placeholder for the agent's internal scratchpad.
prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a friendly and helpful assistant named Snello."
        "Your goal is to help the user manage their to-do list and have a pleasant conversation."
        "If you don't know the user's name, you should ask for it and save it using the 'save_user_name' tool."
        "Once you know their name, you should use it in your responses."
        "You have access to a to-do list manager."
    )),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# --- 4. Create the Agent ---
# The `create_tool_calling_agent` function creates an agent that can use the provided tools.
# It combines the LLM, the prompt, and the tools into a single runnable agent.
agent = create_tool_calling_agent(llm, tools, prompt)

# --- 5. Create the Agent Executor ---
# The `AgentExecutor` is responsible for running the agent and handling the conversation flow.
# It takes the agent and the tools as input.
# `verbose=True` allows us to see the agent's thought process in the console.
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True # Set to True to see the agent's thought process
)
