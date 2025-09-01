import os
from typing import Annotated
from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


checkpointer = InMemorySaver()

os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
os.environ["OPENAI_API_VERSION"] = "2024-02-01"

# Initialize the LLM
llm = init_chat_model(
    "azure_openai:gpt-4.1",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)

# Define some example tools for the agent
@tool
def get_current_time():
    """Get the current time and date."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def calculate(expression: str):
    """Calculate the result of a mathematical expression."""
    try:
        # Safe evaluation of mathematical expressions
        allowed_names = {
            'abs': abs, 'round': round, 'min': min, 'max': max,
            'sum': sum, 'pow': pow, 'divmod': divmod
        }
        code = compile(expression, '<string>', 'eval')
        for name in code.co_names:
            if name not in allowed_names and name not in ['__builtins__']:
                raise NameError(f"Use of {name} not allowed")
        return eval(expression, {"__builtins__": {}}, allowed_names)
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"

# Create the ReAct agent with tools
agent = create_react_agent(
    tools=[get_current_time, calculate],
    model="azure_openai:gpt-4.1",
    checkpointer=checkpointer  
)

def stream_agent_updates(user_input: str):
    """Get the agent's response using invoke."""
    print("\n--- Agent Response ---")
    try:
        config = {"configurable": {"thread_id": "1"}}
        result = agent.invoke({"messages": [{"role": "user", "content": user_input}]}, config)
        
        # Print the final response
        if "messages" in result and result["messages"]:
            final_message = result["messages"][-1]
            if hasattr(final_message, 'content'):
                print(f"Assistant: {final_message.content}")
            else:
                print(f"Assistant: {final_message}")
        
        # Print intermediate steps if available
        if "intermediate_steps" in result and result["intermediate_steps"]:
            print(f"\nReasoning Steps:")
            for step in result["intermediate_steps"]:
                print(f"- {step}")
                
    except Exception as e:
        print(f"Error getting response: {e}")

def main():
    print("Welcome to the LangGraph ReAct Agent!")
    print("This agent can reason through problems and use tools to help you.")
    print("Type 'quit', 'exit', or 'q' to exit.\n")
    
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            stream_agent_updates(user_input)
            print()  # Add spacing between interactions
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()