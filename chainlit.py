import chainlit as cl
from typing import cast
import asyncio

from agent.app import create_agent_with_mcp, invoke_agent, get_agent_response


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
    
    # Get the site information from user session
    site = cl.user_session.get("site")
    
    # Create a message to stream the response
    msg = cl.Message(content="")
    
    try:
        # Get the response from the agent with site context
        response = await get_agent_response(message.content, agent, site=site)        
        await cl.Message(content=response).send()
        
    except Exception as e:
        await msg.update(content=f"❌ Error: {str(e)}")


@cl.on_window_message
async def window_message(message: str):
    """Handle window messages and store site information."""
    try:
        # Extract site information from the message
        site = message.get('site')
        
        if site:
            # Store the site information in the user session
            cl.user_session.set("site", site)
            
            # Send confirmation message
            await cl.Message(
                content=f"✅ Site information received and stored: {site}",
                author="System"
            ).send()
        else:
            await cl.Message(
                content="⚠️ No site information found in window message",
                author="System"
            ).send()
            
    except Exception as e:
        await cl.Message(
            content=f"❌ Error processing window message: {str(e)}",
            author="System"
        ).send()