# Healthcare FHIR Agent

AI-powered healthcare agent for retrieving and analyzing patient data from FHIR R4 servers. Built with LangGraph, OpenAI, and Chainlit.

## Features

- Natural language interface for FHIR data retrieval
- Supports Patient, Observation, Condition, Encounter, and MedicationRequest resources
- Tool-first architecture to prevent hallucination
- Search, create, and update FHIR resources

## Setup

### Prerequisites

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation

```bash
# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Configuration

Required environment variables in `.env`:
```
OPENAI_API_KEY=your-api-key
FHIR_BASE_URL=https://hapi.fhir.org/baseR4
OPENAI_MODEL=gpt-4
```

### Run

```bash
uv run chainlit run app.py
```

Access the UI at `http://localhost:8000`

## Usage Examples

**Patient Data Queries:**
```
Get all data for patient 592598
What observations does patient 592598 have?
Show me conditions for patient 1234567
Get medications for patient 592598
```

**Search Operations:**
```
Search for patients with family name Smith
Find patients named John Doe
```

**Create/Update Resources:**
```
Create a new patient with name John Doe, gender male, birthdate 1990-01-01
Update patient 12345 with new address
Create a blood pressure observation for patient 12345
```


## Supported FHIR Resources

- **Patient**: Demographics, contact info, identifiers
- **Observation**: Vital signs, lab results, measurements
- **Condition**: Diagnoses, medical conditions
- **Encounter**: Visits, hospitalizations, appointments
- **MedicationRequest**: Prescriptions, medication orders


## Architecture

The agent uses a multi-node workflow with LangGraph:

1. **Intent Classifier**: Analyzes queries to determine intent and required FHIR resources
2. **Agent**: Executes FHIR API calls using LangChain tools and GPT-4
3. **Response Formatter**: Converts FHIR JSON data into human-readable responses

### Anti-Hallucination Design

- Tool-first architecture: Agent must fetch data before responding
- Strict system prompts: Never make up data, only use tool results
- Result verification: Responses generated strictly from FHIR API data
- Clear error messaging: Explicitly states when data is unavailable

## Technologies

- **LangGraph**: Agent workflow orchestration
- **LangChain**: LLM framework and tools
- **OpenAI**: GPT-4 for natural language understanding
- **Chainlit**: Interactive chat UI
- **FHIR R4**: Healthcare data standard
- **Python 3.12+**: Core runtime

## Testing

Run tests:

```bash
uv run pytest tests/
```

## Security & Privacy

- ⚠️ The public FHIR server is for **testing and learning only**
- ⚠️ Never use real Protected Health Information (PHI)
- ⚠️ For production, implement authentication and HIPAA compliance
- ℹ️ This is a demonstration system, not for clinical use

## Medical Disclaimer

**IMPORTANT**: This agent is for educational and demonstration purposes only. It does NOT provide medical advice, diagnosis, or treatment recommendations. Always consult qualified healthcare professionals for medical decisions.

