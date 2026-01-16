"""State definitions for the LangGraph agent."""
from typing import TypedDict, List, Optional, Dict, Any, Annotated
import operator


class AgentState(TypedDict):
    """State for the healthcare agent graph."""

    # User input and conversation
    messages: Annotated[List[Dict[str, str]], operator.add]
    user_query: str

    # Intent and routing
    intent: Optional[str]
    resource_type: Optional[str]
    operation: Optional[str]  # create, read, update, delete, search

    # FHIR data
    fhir_params: Optional[Dict[str, Any]]
    fhir_response: Optional[Dict[str, Any]]

    # Agent output
    agent_response: Optional[str]
    error: Optional[str]

    # Metadata
    iteration_count: int

