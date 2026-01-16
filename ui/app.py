"""Chainlit application for the healthcare agent."""
import chainlit as cl
from agents.graph import healthcare_graph
from agents.state import AgentState
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session."""
    # Initialize conversation history in user session
    cl.user_session.set("conversation_history", [])

    # Send welcome message
    welcome_message = """AI assistant for retrieving patient data from FHIR R4 servers.

**What I can retrieve:**
- Patient demographics, observations, conditions, encounters, medications

**Example queries:**
- "Get all data for patient 592598"
- "Show me observations for patient 1234567"
- "Search for patients with family name Smith"

**Note:** Data retrieved from https://hapi.fhir.org/baseR4 (test server). No medical advice provided.
"""

    await cl.Message(content=welcome_message).send()


@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming messages."""
    user_query = message.content

    # Get conversation history
    conversation_history = cl.user_session.get("conversation_history", [])

    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_query
    })

    # Show processing message
    processing_msg = cl.Message(content="Processing...")
    await processing_msg.send()

    try:
        # Create initial state
        initial_state: AgentState = {
            "messages": conversation_history.copy(),
            "user_query": user_query,
            "intent": None,
            "resource_type": None,
            "operation": None,
            "fhir_params": None,
            "fhir_response": None,
            "agent_response": None,
            "error": None,
            "iteration_count": 0
        }

        # Run the graph
        result = healthcare_graph.invoke(initial_state)

        # Extract response
        agent_response = result.get("agent_response", "I apologize, but I couldn't process your request.")

        # Add assistant message to history
        conversation_history.append({
            "role": "assistant",
            "content": agent_response
        })

        # Update session
        cl.user_session.set("conversation_history", conversation_history)

        # Update the processing message with the actual response
        processing_msg.content = agent_response
        await processing_msg.update()

        # Log intent for debugging
        intent = result.get("intent")
        if intent:
            logger.info(f"Processed query with intent: {intent}")

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        error_message = f"Error: {str(e)}\n\nPlease try again or rephrase your question."
        processing_msg.content = error_message
        await processing_msg.update()


@cl.on_chat_end
async def on_chat_end():
    """Handle chat session end."""
    logger.info("Chat session ended")


if __name__ == "__main__":
    # This won't run directly, use: chainlit run app.py
    pass

