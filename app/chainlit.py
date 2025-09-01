import chainlit as cl
from typing import cast
import asyncio
import sys
import os

# Add the agent directory to the path so we can import from app.py
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agent'))

from app import create_agent_with_mcp, invoke_agent, get_agent_response


@cl.on_chat_start
async def on_chat_start():
    """Initialize the agent when the chat starts."""
    # Show a loading message
    await cl.Message(
        content="Initializing the ReAct agent with MCP tools...",
        author="System"
    ).send()
    
    try:
        # Create the agent
        agent = await create_agent_with_mcp()
        
        # Store the agent in the user session
        cl.user_session.set("agent", agent)
        
        # Send success message
        await cl.Message(
            content="✅ Agent initialized successfully! I'm ready to help you with reasoning tasks and can use various tools including MCP server tools.",
            author="System"
        ).send()
        
    except Exception as e:
        await cl.Message(
            content=f"❌ Failed to initialize agent: {str(e)}",
            author="System"
        ).send()


@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming messages and get responses from the agent."""
    # Get the agent from user session
    agent = cl.user_session.get("agent")
    
    if not agent:
        await cl.Message(
            content="❌ Agent not initialized. Please refresh the page and try again.",
            author="System"
        ).send()
        return
    
    # Create a message to stream the response
    msg = cl.Message(content="")
    await msg.send()
    
    try:
        # Get the response from the agent
        response = await get_agent_response(message.content, agent)
        
        # Stream the response
        for chunk in response.split():
            await msg.stream_token(chunk + " ")
            await asyncio.sleep(0.05)  # Small delay for better streaming effect
        
        await msg.update()
        
    except Exception as e:
        await msg.update(content=f"❌ Error: {str(e)}")
