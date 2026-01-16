"""Node functions for the LangGraph healthcare agent."""
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from agents.state import AgentState
from agents.tools import healthcare_tools
from config import OPENAI_API_KEY, OPENAI_MODEL
import logging
import json

logger = logging.getLogger(__name__)

# Initialize LLM
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model=OPENAI_MODEL,
    temperature=0.7
)

# Bind tools to LLM
llm_with_tools = llm.bind_tools(healthcare_tools)


def intent_classifier_node(state: AgentState) -> Dict[str, Any]:
    """Classify user intent and determine routing.

    Args:
        state: Current agent state

    Returns:
        Updated state with intent classification
    """
    user_query = state.get("user_query", "")

    classification_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a healthcare intent classifier for a FHIR data retrieval system.

Analyze the user's query and determine:
1. The intent (greeting, patient_data_query, search_query, general_question, clarification_needed)
2. The resource type if applicable (Patient, Observation, Condition, Encounter, MedicationRequest, All)
3. The operation type (read, search, create, update)

IMPORTANT:
- If the query mentions a patient ID or asks for patient data, set intent to "patient_data_query"
- If asking for "all data" or "everything" about a patient, set resource_type to "All"
- If the query is unclear or missing required info (like patient ID), set intent to "clarification_needed"

Respond in JSON format:
{"intent": "...", "resource_type": "...", "operation": "...", "requires_clarification": false}

Examples:
- "Get all data for patient 592598" -> {"intent": "patient_data_query", "resource_type": "All", "operation": "read"}
- "Show observations for patient 123" -> {"intent": "patient_data_query", "resource_type": "Observation", "operation": "read"}
- "What conditions does patient 456 have?" -> {"intent": "patient_data_query", "resource_type": "Condition", "operation": "read"}
- "Search for patients named Smith" -> {"intent": "search_query", "resource_type": "Patient", "operation": "search"}
- "Tell me about a patient" -> {"intent": "clarification_needed", "requires_clarification": true}
"""),
        ("human", "{query}")
    ])

    try:
        response = llm.invoke(classification_prompt.format_messages(query=user_query))
        classification = json.loads(response.content)

        return {
            "intent": classification.get("intent"),
            "resource_type": classification.get("resource_type"),
            "operation": classification.get("operation"),
            "messages": [{"role": "assistant", "content": f"Classified intent: {classification.get('intent')}"}]
        }
    except Exception as e:
        logger.error(f"Error in intent classification: {e}")
        return {
            "intent": "general_question",
            "error": str(e),
            "messages": [{"role": "assistant", "content": "Processing your request..."}]
        }


def agent_node(state: AgentState) -> Dict[str, Any]:
    """Main agent node that uses tools to fulfill user requests.

    Args:
        state: Current agent state

    Returns:
        Updated state with agent actions
    """
    user_query = state.get("user_query", "")
    intent = state.get("intent", "")
    messages = state.get("messages", [])

    # Build conversation history
    conversation = []
    for msg in messages[-10:]:  # Keep last 10 messages for context
        if msg.get("role") == "user":
            conversation.append(HumanMessage(content=msg.get("content", "")))
        elif msg.get("role") == "assistant":
            conversation.append(AIMessage(content=msg.get("content", "")))

    # Add current query
    conversation.append(HumanMessage(content=user_query))

    system_prompt = """You are a FHIR healthcare data assistant. You MUST follow these strict rules:

CRITICAL RULES - NEVER VIOLATE:
1. NEVER hallucinate or make up patient data
2. ONLY provide information that comes directly from FHIR API calls via tools
3. If data is not available from the API, explicitly state "This information is not available in the FHIR system"
4. ALWAYS use tools to fetch data before answering patient-specific questions
5. NEVER provide medical diagnosis or medical advice
6. If a query is ambiguous, ask clarifying questions

WHAT YOU CAN DO:
- Retrieve patient demographics from the FHIR server
- Fetch observations, conditions, encounters, and medication requests
- Search for patients
- Explain FHIR resources and healthcare data standards
- Answer general questions about the system's capabilities

WHAT YOU CANNOT DO:
- Diagnose medical conditions
- Recommend treatments or medications
- Make up or infer patient data that wasn't retrieved from FHIR
- Provide medical advice

DATA RETRIEVAL:
- Always fetch fresh data from the FHIR server using the provided tools
- If data is missing, say "No [resource type] data found for this patient"
- Format responses in a clear, human-readable way
- Include relevant context from the FHIR data

MEDICAL DISCLAIMER:
Always remind users that you cannot provide medical advice and that they should consult healthcare professionals for medical decisions.

When creating or updating FHIR resources, ensure the data follows FHIR R4 specifications.
"""

    full_messages = [SystemMessage(content=system_prompt)] + conversation

    try:
        # Invoke LLM with tools
        response = llm_with_tools.invoke(full_messages)

        # Check if tools were called
        if hasattr(response, 'tool_calls') and response.tool_calls:
            tool_results = []
            for tool_call in response.tool_calls:
                # Execute tool
                tool_name = tool_call.get('name')
                tool_args = tool_call.get('args', {})

                logger.info(f"Executing tool: {tool_name} with args: {tool_args}")

                # Find and execute the tool
                for tool in healthcare_tools:
                    if tool.name == tool_name:
                        result = tool.invoke(tool_args)
                        tool_results.append(f"Tool: {tool_name}\nResult: {result}")
                        break

            # Generate final response based on tool results
            tool_summary = "\n\n".join(tool_results)
            final_prompt = f"""Based STRICTLY on the following tool execution results, provide a clear, accurate, human-readable response.

TOOL RESULTS:
{tool_summary}

USER QUERY: {user_query}

INSTRUCTIONS:
- Use ONLY the data from the tool results above
- Do NOT make up or infer any information
- If data is missing or not found, explicitly state that
- Format the response in a clear, conversational way
- Include a medical disclaimer if relevant
- If the query cannot be answered with the available data, say so clearly"""

            final_response = llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=final_prompt)
            ])
            agent_response = final_response.content
        else:
            agent_response = response.content

        return {
            "agent_response": agent_response,
            "messages": [{"role": "assistant", "content": agent_response}],
            "iteration_count": state.get("iteration_count", 0) + 1
        }
    except Exception as e:
        logger.error(f"Error in agent node: {e}")
        error_msg = f"I apologize, but I encountered an error while trying to fetch data from the FHIR server: {str(e)}"
        return {
            "agent_response": error_msg,
            "error": str(e),
            "messages": [{"role": "assistant", "content": error_msg}]
        }


def response_formatter_node(state: AgentState) -> Dict[str, Any]:
    """Format the final response for the user.

    Args:
        state: Current agent state

    Returns:
        Updated state with formatted response
    """
    agent_response = state.get("agent_response", "")
    error = state.get("error")

    if error:
        formatted_response = f"⚠️ {agent_response}"
    else:
        formatted_response = agent_response

    return {
        "agent_response": formatted_response,
        "messages": [{"role": "assistant", "content": formatted_response}]
    }

