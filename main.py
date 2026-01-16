"""
Healthcare LangGraph Agent - Main Entry Point

This module provides a command-line interface to run the healthcare agent.
For the full Chainlit UI experience, run: chainlit run app.py
"""
from agents.graph import healthcare_graph
import logging
logger = logging.getLogger(__name__)
    run_agent_cli()

    print("\nStarting CLI Mode...\n")
    print("2. Chainlit UI Mode - Run: chainlit run app.py")
    print("1. CLI Mode (current)")
    print("\nStartup Options:")
    print("=" * 50)
    print("Healthcare LangGraph Agent")
    print("\n" + "=" * 50)
            logger.error(f"Error: {e}", exc_info=True)
        except Exception as e:
            break
            print("\n\n👋 Goodbye! Stay healthy!")
        except KeyboardInterrupt:

            print(f"\n🤖 Agent: {agent_response}")
            # Display response

            })
                "content": agent_response
                "role": "assistant",
            conversation_history.append({
            # Add to history

            agent_response = result.get("agent_response", "I couldn't process your request.")
            # Get response

            result = healthcare_graph.invoke(initial_state)
            print("\n🤔 Processing...")
            # Run the graph

            }
                "iteration_count": 0
                "error": None,
                "agent_response": None,
                "fhir_response": None,
                "fhir_params": None,
                "operation": None,
                "resource_type": None,
                "intent": None,
                "user_query": user_input,
                "messages": conversation_history.copy(),
            initial_state: AgentState = {
            # Create initial state

            })
                "content": user_input
                "role": "user",
            conversation_history.append({
            # Add to conversation history

                break
                print("\n👋 Goodbye! Stay healthy!")
            if user_input.lower() in ['exit', 'quit', 'q']:

                continue
            if not user_input:

            user_input = input("\n👤 You: ").strip()
            # Get user input
        try:
    while True:

    conversation_history = []

    print("Type 'exit' or 'quit' to end the session\n")
    print("=" * 50)
    print("🏥 Healthcare Agent - CLI Mode")
    """Run the agent in command-line mode."""
def run_agent_cli():
from agents.state import AgentState


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
