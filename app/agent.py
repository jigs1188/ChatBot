import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if API key is available for OpenRouter
openrouter_key = os.getenv("OPENROUTER_API_KEY")
google_key = os.getenv("GOOGLE_API_KEY")

if not openrouter_key and not google_key:
    print(
        "Warning: No API key found. Please set OPENROUTER_API_KEY or GOOGLE_API_KEY in your .env file."
    )

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from app.tools import (
    add_todo,
    remove_todo,
    list_todos,
    complete_todo,
    save_user_name,
    get_user_name,
    clear_todos,
    count_todos,
    get_analytics,
    search_todos,
    get_motivational_quote,
    set_reminder,
)

# --- 1. Load the LLM ---
# Using OpenRouter for free API access with multiple model options
try:
    if openrouter_key:
        llm = ChatOpenAI(
            model="deepseek/deepseek-chat",  # DeepSeek V3.1 - Free model on OpenRouter
            openai_api_key=openrouter_key,
            openai_api_base="https://openrouter.ai/api/v1",
            headers={
                "HTTP-Referer": "https://snello-ai.com",
                "X-Title": "Snello AI Assistant",
            },
            temperature=0.7,
            max_tokens=2000,
        )
        print("✅ Using DeepSeek V3.1 via OpenRouter")
    else:
        # Fallback to Google Gemini if available
        from langchain_google_genai import ChatGoogleGenerativeAI

        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", convert_system_message_to_human=True
        )

except Exception as e:
    print(f"Error initializing LLM: {e}")

    # Create a mock LLM for development
    class MockLLM:
        def invoke(self, *args, **kwargs):
            return "I'm a demo AI assistant. Please configure your API key to enable full functionality."

    llm = MockLLM()

# --- 2. Define the Tools ---
# The tools are the functions the agent can call to interact with the outside world.
# Advanced tools for comprehensive task management and user interaction.
tools = [
    add_todo,
    remove_todo,
    list_todos,
    complete_todo,
    save_user_name,
    get_user_name,
    clear_todos,
    count_todos,
    get_analytics,
    search_todos,
    get_motivational_quote,
    set_reminder,
]

# --- 3. Create the Prompt ---
# The prompt is the set of instructions that guides the agent's behavior.
# It includes a system message, placeholders for chat history and user input,
# and a placeholder for the agent's internal scratchpad.
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are Snello, an advanced AI-powered personal assistant with exceptional capabilities."
                " You're designed to be intelligent, helpful, proactive, and engaging."
                " Your core features include:"
                " 🎯 Advanced task management with priorities and analytics"
                " 💬 Natural conversation with memory and context awareness"
                " 📊 Productivity insights and motivational support"
                " 🔍 Smart search and organization capabilities"
                " "
                " Personality traits:"
                " • Be enthusiastic and encouraging"
                " • Use appropriate emojis to make interactions lively"
                " • Provide detailed, actionable responses"
                " • Offer proactive suggestions and insights"
                " • Remember user preferences and context"
                " "
                " When users interact with you:"
                " • If you don't know their name, politely ask and save it"
                " • Use their name naturally in conversations"
                " • Provide clear confirmation of all actions taken"
                " • Offer additional related suggestions when appropriate"
                " • Use formatting and emojis to make responses visually appealing"
                " "
                " For task management:"
                " • Automatically detect priority levels from user language"
                " • Suggest productivity tips and insights"
                " • Celebrate completions and progress"
                " • Provide detailed analytics when requested"
            ),
        ),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

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
    verbose=True,  # Set to True to see the agent's thought process
)


def get_agent_executor():
    """Return the configured agent executor"""
    return agent_executor
