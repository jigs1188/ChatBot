
from app.agent import agent_executor
from langchain_core.messages import HumanMessage, AIMessage

# In-memory store for conversation history
chat_history = []

def main():
    """Main function to run the chatbot CLI."""
    print("Welcome to Snello! Your personal AI assistant.")
    print("You can ask me to manage your to-do list or just chat.")
    print("Type 'exit' to end the conversation.")

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break

            # Invoke the agent with the user input and chat history
            response = agent_executor.invoke({
                "input": user_input,
                "chat_history": chat_history
            })

            # Append the conversation to history
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=response["output"]))

            print(f"\nSnello: {response['output']}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
