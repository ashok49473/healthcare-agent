"""LangGraph definition for the healthcare agent."""
from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.nodes import intent_classifier_node, agent_node, response_formatter_node
import logging

logger = logging.getLogger(__name__)


def create_healthcare_graph():
    """Create and compile the healthcare agent graph.

    Returns:
        Compiled LangGraph
    """
    # Create the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("intent_classifier", intent_classifier_node)
    workflow.add_node("agent", agent_node)
    workflow.add_node("response_formatter", response_formatter_node)

    # Define routing logic
    def route_after_intent(state: AgentState) -> str:
        """Route based on classified intent."""
        intent = state.get("intent", "")

        # For greetings, we might skip tool usage
        if intent == "greeting":
            return "agent"

        # For all other intents, go to agent
        return "agent"

    def route_after_agent(state: AgentState) -> str:
        """Route after agent processing."""
        error = state.get("error")
        iteration_count = state.get("iteration_count", 0)

        # If max iterations reached, format and end
        if iteration_count >= 5:
            logger.warning("Max iterations reached")
            return "response_formatter"

        # Normal flow: format response
        return "response_formatter"

    # Add edges
    workflow.set_entry_point("intent_classifier")
    workflow.add_conditional_edges(
        "intent_classifier",
        route_after_intent,
        {
            "agent": "agent",
        }
    )
    workflow.add_conditional_edges(
        "agent",
        route_after_agent,
        {
            "response_formatter": "response_formatter",
        }
    )
    workflow.add_edge("response_formatter", END)

    # Compile the graph
    app = workflow.compile()

    logger.info("Healthcare agent graph compiled successfully")
    return app


# Create the graph instance
healthcare_graph = create_healthcare_graph()

