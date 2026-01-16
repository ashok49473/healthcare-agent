"""Chainlit application for the healthcare agent."""
import chainlit as cl
from agents.graph import healthcare_graph
from agents.state import AgentState
import logging
from typing import Dict, Any

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
    welcome_message = """# 🏥 FHIR Healthcare Data Assistant

Welcome! I'm your AI assistant for retrieving and analyzing healthcare data from the FHIR R4 server.

## 🎯 What I Can Do

I can help you retrieve **real patient data** from the public FHIR server by:

- 📋 **Patient Demographics**: Get patient information by ID
- 🔬 **Observations**: View vital signs, lab results, and measurements  
- 🏥 **Conditions**: See diagnoses and medical conditions
- 👨‍⚕️ **Encounters**: Check medical visits and appointments
- 💊 **Medications**: Review medication requests and prescriptions
- 🔍 **Complete Summary**: Get all data for a patient at once

## 📝 How to Use

Simply provide a **patient ID** and ask your question:

**Examples:**
- "Get all data for patient 592598"
- "Show me observations for patient 1234567"
- "What conditions does patient 592598 have?"
- "Search for patients with family name Smith"

## ⚠️ Important Notes

- ✅ All data comes from: **https://hapi.fhir.org/baseR4**
- ✅ I only provide information from actual FHIR data
- ❌ I do **NOT** provide medical diagnosis or advice
- ❌ I will **NOT** make up or guess patient data
- ℹ️ If data is unavailable, I'll clearly tell you

💡 **Tip**: Try patient ID **592598** - it's a test patient with sample data!

---

**Need help?** Just ask me to explain what I can do!
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
    processing_msg = cl.Message(content="🤔 Processing your request...")
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
        error_message = f"❌ An error occurred: {str(e)}\n\nPlease try again or rephrase your question."
        processing_msg.content = error_message
        await processing_msg.update()


@cl.on_chat_end
async def on_chat_end():
    """Handle chat session end."""
    logger.info("Chat session ended")


if __name__ == "__main__":
    # This won't run directly, use: chainlit run app.py
    pass

