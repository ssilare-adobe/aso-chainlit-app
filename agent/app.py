"""
ASO Chainlit App - LangGraph ReAct Agent

This module implements a ReAct (Reasoning and Acting) agent using LangGraph and Azure OpenAI.
The agent can reason through problems, use tools, and provide intelligent responses.

Key Components:
- ReAct Agent: Uses LangGraph for reasoning and acting capabilities
- Tool Integration: Built-in tools + MCP server tools
- Memory Management: In-memory checkpointing for conversation continuity
- Dual Interface Support: Functions for both CLI and Chainlit web interface

Author: ASO Team
"""

import os
import asyncio
from typing import Annotated, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# LangChain and LangGraph imports for agent functionality
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient

# Initialize in-memory checkpointing for conversation state management
checkpointer = InMemorySaver()

# Set up Azure OpenAI environment variables
os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
os.environ["OPENAI_API_VERSION"] = "2024-02-01"

# Initialize the Azure OpenAI language model (GPT-4.1)
# This is the core LLM that powers the agent's reasoning capabilities
llm = init_chat_model(
    "azure_openai:gpt-4.1",
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)

# Initialize MCP (Model Context Protocol) client for external tool integration
# Connects to a local MCP server running on localhost:3000
mcp_client = MultiServerMCPClient(
    {
        "mcp_server": {
            "url": "http://localhost:3000/mcp",
            "transport": "streamable_http",
            "headers": {
                "Accept": "application/json, text/event-stream",
                "x-api-key": os.getenv("X_API_KEY"),  # API key for MCP server authentication
            }
        }
    }
)

# =============================================================================
# MCP TOOL INTEGRATION
# =============================================================================

async def get_mcp_tools():
    """
    Retrieve tools from the MCP (Model Context Protocol) server.
    
    This function connects to the local MCP server and fetches available tools.
    If the connection fails, it gracefully falls back to local tools only.
    
    Returns:
        list: List of MCP tools or empty list if connection fails
        
    Note:
        MCP tools provide additional capabilities like file operations,
        web searches, database queries, etc., depending on server configuration.
    """
    try:
        tools = await mcp_client.get_tools()
        return tools
    except Exception as e:
        print(f"Warning: Could not connect to MCP server: {e}")
        return []

# =============================================================================
# AGENT CREATION AND MANAGEMENT
# =============================================================================

async def create_agent_with_mcp():
    """
    Create a ReAct agent with integrated MCP tools.
    
    This function initializes a LangGraph ReAct agent that combines:
    - MCP server tools (if available)
    - Azure OpenAI GPT-4.1 for reasoning
    
    Returns:
        Agent: Configured ReAct agent ready for use
        
    ReAct Architecture:
        - Reasoning: Agent analyzes user input and determines required actions
        - Acting: Agent executes appropriate tools based on reasoning
        - Iteration: Process continues until a satisfactory response is generated
    """
    # Fetch available MCP tools
    mcp_tools = await get_mcp_tools()
    
    # Combine local tools with MCP tools
    all_tools = mcp_tools
    
    # Create the ReAct agent with all available tools
    agent = create_react_agent(
        tools=all_tools,
        model="azure_openai:gpt-4.1",
        checkpointer=checkpointer,  # Enable conversation memory
    )
    return agent

# =============================================================================
# AGENT INVOCATION FUNCTIONS
# =============================================================================

async def invoke_agent(user_input: str, agent, thread_id: str = "1") -> Dict[str, Any]:
    """
    Invoke the agent with user input and return the complete result.
    
    This function is the core interface for interacting with the agent.
    It handles the agent invocation and returns the full response including
    intermediate steps and reasoning.
    
    Args:
        user_input (str): User's question or request
        agent: The ReAct agent instance
        thread_id (str): Conversation thread identifier for memory management
        
    Returns:
        Dict[str, Any]: Complete agent response including:
            - messages: List of conversation messages
            - intermediate_steps: Agent's reasoning and tool usage steps
            - error: Error message if invocation fails
            
    Usage:
        This function is primarily used by get_agent_response() and
        can be imported by external interfaces like Chainlit.
    """
    try:
        # Configure the agent with thread-specific memory
        config = {"configurable": {"thread_id": thread_id}}
        
        # Invoke the agent with the user's input
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]}, 
            config
        )
        return result
    except Exception as e:
        return {"error": str(e)}

async def get_agent_response(user_input: str, agent, thread_id: str = "1", site: str = None) -> str:
    """
    Get a formatted text response from the agent.
    
    This function provides a simplified interface that returns only the
    final response text, suitable for web interfaces and user display.
    
    Args:
        user_input (str): User's question or request
        agent: The ReAct agent instance
        thread_id (str): Conversation thread identifier
        site (str): Site information for context
        
    Returns:
        str: Formatted response text or error message
        
    Usage:
        This is the main function used by Chainlit and other web interfaces
        to get clean, displayable responses from the agent.
    """
    # Enhance user input with site context if available
    if site:
        enhanced_input = f"""Site: {site}

        User Question: {user_input}"""
    else:
        enhanced_input = user_input
    
    # Get the complete agent result
    print(enhanced_input)
    result = await invoke_agent(enhanced_input, agent, thread_id)
    
    # Handle errors gracefully
    if "error" in result:
        return f"Error: {result['error']}"
    
    # Extract the final response from the agent's messages
    if "messages" in result and result["messages"]:
        final_message = result["messages"][-1]
        if hasattr(final_message, 'content'):
            print(final_message.content)
            return final_message.content
        else:
            return str(final_message)
    
    return "No response generated."

# =============================================================================
# CLI INTERFACE FUNCTIONS
# =============================================================================

async def stream_agent_updates(user_input: str, agent):
    """
    Display agent response with detailed reasoning steps (CLI interface).
    
    This function is designed for the command-line interface and provides
    detailed output including the agent's reasoning process and tool usage.
    
    Args:
        user_input (str): User's question or request
        agent: The ReAct agent instance
        
    Output:
        Prints to console:
        - Final response from the agent
        - Intermediate reasoning steps
        - Tool usage details
    """
    print("\n--- Agent Response ---")
    try:
        # Use default thread for CLI interactions
        config = {"configurable": {"thread_id": "1"}}
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]}, 
            config
        )
        
        # Display the final response
        if "messages" in result and result["messages"]:
            final_message = result["messages"][-1]
            if hasattr(final_message, 'content'):
                print(f"Assistant: {final_message.content}")
            else:
                print(f"Assistant: {final_message}")
        
        # Display intermediate reasoning steps for transparency
        if "intermediate_steps" in result and result["intermediate_steps"]:
            print(f"\nReasoning Steps:")
            for step in result["intermediate_steps"]:
                print(f"- {step}")
                
    except Exception as e:
        print(f"Error getting response: {e}")

# =============================================================================
# MAIN CLI APPLICATION
# =============================================================================

async def main():
    """
    Main CLI application entry point.
    
    This function provides an interactive command-line interface for
    testing and using the ReAct agent. It demonstrates the agent's
    capabilities and provides a development/testing environment.
    
    Features:
        - Interactive chat interface
        - MCP server connection status
        - Tool availability display
        - Graceful error handling
        - Easy exit commands
    """
    print("Welcome to the LangGraph ReAct Agent with MCP Integration!")
    print("This agent can reason through problems and use tools from the MCP server at localhost:3000.")
    print("Type 'quit', 'exit', or 'q' to exit.\n")
    
    # Test MCP connection and display available tools
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
    
    # Initialize the agent with all available tools
    print("\nInitializing agent...")
    agent = await create_agent_with_mcp()
    print("✅ Agent initialized successfully!")
    print()
    
    # Main interaction loop
    while True:
        try:
            # Get user input
            user_input = input("User: ")
            
            # Check for exit commands
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
                
            # Process the input through the agent
            await stream_agent_updates(user_input, agent)
            print()  # Add spacing between interactions
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

# Entry point for CLI execution
if __name__ == "__main__":
    asyncio.run(main())