import os
import asyncio
from typing import Annotated, Dict, Any
from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient

checkpointer = InMemorySaver()

os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
os.environ["OPENAI_API_VERSION"] = "2024-02-01"

# Initialize the LLM
llm = init_chat_model(
    "azure_openai:gpt-4.1",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)

# Initialize MCP client to connect to localhost:3000
mcp_client = MultiServerMCPClient(
    {
        "mcp_server": {
            "url": "http://localhost:3000/mcp",
            "transport": "streamable_http",
            "headers": {
                "Accept": "application/json, text/event-stream",
                "x-api-key": os.getenv("X_API_KEY"),
            }
        }
    }
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

async def get_mcp_tools():
    """Get tools from the MCP server."""
    try:
        tools = await mcp_client.get_tools()
        return tools
    except Exception as e:
        print(f"Warning: Could not connect to MCP server: {e}")
        return []

async def create_agent_with_mcp():
    """Create the ReAct agent with MCP tools."""
    mcp_tools = await get_mcp_tools()
    
    # Combine MCP tools with local tools
    all_tools = [get_current_time, calculate] + mcp_tools
    
    # Create the ReAct agent with all tools
    agent = create_react_agent(
        tools=all_tools,
        model="azure_openai:gpt-4.1",
        checkpointer=checkpointer,
    )
    return agent

async def invoke_agent(user_input: str, agent, thread_id: str = "1") -> Dict[str, Any]:
    """Invoke the agent with user input and return the result."""
    try:
        config = {"configurable": {"thread_id": thread_id}}
        result = await agent.ainvoke({"messages": [{"role": "user", "content": user_input}]}, config)
        return result
    except Exception as e:
        return {"error": str(e)}

async def get_agent_response(user_input: str, agent, thread_id: str = "1") -> str:
    """Get a formatted response from the agent."""
    result = await invoke_agent(user_input, agent, thread_id)
    
    if "error" in result:
        return f"Error: {result['error']}"
    
    # Extract the final response
    if "messages" in result and result["messages"]:
        final_message = result["messages"][-1]
        if hasattr(final_message, 'content'):
            return final_message.content
        else:
            return str(final_message)
    
    return "No response generated."

async def stream_agent_updates(user_input: str, agent):
    """Get the agent's response using ainvoke."""
    print("\n--- Agent Response ---")
    try:
        config = {"configurable": {"thread_id": "1"}}
        result = await agent.ainvoke({"messages": [{"role": "user", "content": user_input}]}, config)
        
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

async def main():
    print("Welcome to the LangGraph ReAct Agent with MCP Integration!")
    print("This agent can reason through problems and use tools from the MCP server at localhost:8080.")
    print("Type 'quit', 'exit', or 'q' to exit.\n")
    
    # Test MCP connection and create agent once
    try:
        mcp_tools = await get_mcp_tools()
        if mcp_tools:
            print(f"✅ Connected to MCP server! Available tools: {len(mcp_tools)}")
            for tool in mcp_tools:
                print(f"  - {tool.name}: {tool.description}")
        else:
            print("⚠️  MCP server connection failed, but local tools are available")
    except Exception as e:
        print(f"⚠️  MCP server connection failed: {e}")
        print("Local tools will still be available")
    
    # Initialize the agent once with all available tools
    print("\nInitializing agent...")
    agent = await create_agent_with_mcp()
    print("✅ Agent initialized successfully!")
    print()
    
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            await stream_agent_updates(user_input, agent)
            print()  # Add spacing between interactions
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    asyncio.run(main())