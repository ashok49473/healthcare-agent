# Healthcare FHIR Data Agent 🏥

A specialized AI-powered healthcare agent that retrieves and analyzes **real patient data** from the public FHIR R4 server. Built with LangGraph, OpenAI, and Chainlit.

## 🎯 Key Features

- 🔒 **Zero Hallucination**: Only provides data from actual FHIR API calls
- 🏥 **Comprehensive Data**: Fetches Patient, Observation, Condition, Encounter, MedicationRequest resources
- 💬 **Natural Language**: Ask questions about patients in plain English
- 🚫 **No Medical Advice**: Strictly data retrieval, no diagnosis or treatment recommendations
- 🌐 **FHIR R4 Standard**: Uses official healthcare data standard
- 💡 **Smart Clarification**: Asks for clarification when queries are ambiguous

## 🏗️ Architecture

```
HealthCareAgent/
├── agents/
│   ├── __init__.py
│   ├── state.py          # Agent state definitions
│   ├── nodes.py          # Graph node functions (intent, agent, formatter)
│   ├── tools.py          # FHIR interaction tools
│   └── graph.py          # LangGraph workflow definition
├── utils/
│   ├── __init__.py
│   ├── fhir_client.py    # FHIR API client
│   └── fhir_templates.py # FHIR resource templates
├── tests/
│   ├── __init__.py
│   └── test_fhir_client.py
├── app.py                # Chainlit application
├── config.py             # Configuration settings
├── chainlit.md           # About page for UI
├── test_agent.py         # Agent test suite
├── AGENT_BEHAVIOR.md     # Detailed behavior documentation
├── pyproject.toml        # Project dependencies (managed by uv)
└── .env.example          # Environment variables template
```

## 🚀 Getting Started

### 1. Clone and Navigate

```bash
cd HealthCareAgent
```

### 2. Install uv (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Install Dependencies

```bash
uv sync
```

This will automatically create a virtual environment and install all dependencies from `pyproject.toml`.

### 4. Configure Environment

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-openai-api-key-here
FHIR_BASE_URL=https://hapi.fhir.org/baseR4
OPENAI_MODEL=gpt-4
```

### 5. Run the Application

```bash
uv run chainlit run app.py
```

The application will start at `http://localhost:8000`

## 🧪 Try It Out

**Sample Patient ID**: Try **592598** (often has test data on the public server)

Or search for patients to find valid IDs:
```
Search for patients with family name Smith
```

## Usage

### Query Patient Data

The agent is designed for **patient ID-based queries**. Simply provide a patient ID and ask your question:

**Get Complete Patient Summary:**
```
Get all data for patient 592598
Show me everything for patient 1234567
```

**Specific Resource Queries:**
```
What observations does patient 592598 have?
Show me conditions for patient 1234567
Get medications for patient 592598
What are the encounters for patient 1234567?
Get patient demographics for 592598
```

### Search Operations

**Find Patients:**
```
Search for patients with family name Smith
Find patients named John Doe
```

### General Questions

```
What can you do?
Explain FHIR resources
What is the difference between Condition and Observation?
```

## 📋 FHIR Resources Supported

- **Patient**: Demographics, contact info, identifiers
- **Observation**: Vital signs, lab results, measurements
- **Condition**: Diagnoses, medical conditions
- **Encounter**: Visits, hospitalizations, appointments
- **MedicationRequest**: Prescriptions, medication orders

## 🔄 Agent Workflow

The agent uses a sophisticated multi-node workflow:

1. **Intent Classifier**: Analyzes user query, detects patient IDs, identifies required resources
2. **Agent Node**: Executes FHIR API calls via tools, retrieves real data
3. **Response Formatter**: Converts FHIR JSON to human-readable responses

## 🛡️ Agent Behavior Guarantees

### What the Agent DOES:
✅ Retrieves data from **https://hapi.fhir.org/baseR4** only
✅ Provides accurate, data-backed responses
✅ Clearly states when data is unavailable
✅ Asks for clarification on ambiguous queries
✅ Formats technical FHIR data into readable answers

### What the Agent DOES NOT DO:
❌ Hallucinate or make up patient data
❌ Provide medical diagnosis or advice
❌ Infer information not present in FHIR data
❌ Give treatment recommendations
❌ Make clinical decisions

**For detailed information on how hallucination is prevented**, see [AGENT_BEHAVIOR.md](AGENT_BEHAVIOR.md)

## 🔧 Extending the Agent

### Add New FHIR Resources

1. Add tool functions in `agents/tools.py` for new resource types (e.g., AllergyIntolerance, Procedure)
2. Update the `healthcare_tools` list
3. Tools are automatically available to the agent

### Modify Agent Behavior

1. Edit `agents/nodes.py` to adjust the system prompts
2. Update intent classification logic in `intent_classifier_node`
3. Customize response formatting

### Enhance the UI

1. Modify `app.py` for custom welcome messages and chat features
2. Edit `chainlit.md` for the About page
3. Add custom Chainlit actions and elements

## 📚 Technologies

- **LangGraph**: Agent workflow orchestration
- **LangChain**: LLM framework and tools
- **OpenAI**: GPT models for natural language
- **Chainlit**: Interactive chat UI
- **FHIR API**: Healthcare data standard
- **Python 3.12+**: Modern Python features
- **UV**: Fast Python package manager

## 🧪 Testing

Run the agent test suite:

```bash
uv run python test_agent.py
```

This will test various query types and validate agent behavior.

## 🔒 Security & Privacy Notes

- ⚠️ The public FHIR server is for **testing and learning only**
- ⚠️ Never use real Protected Health Information (PHI)
- ⚠️ For production, implement authentication and HIPAA compliance
- ⚠️ Never commit `.env` file with real API keys
- ℹ️ This is a demonstration system, not for clinical use

## ⚕️ Medical Disclaimer

**IMPORTANT**: This agent is for educational and demonstration purposes only. It does NOT provide medical advice, diagnosis, or treatment recommendations. Always consult qualified healthcare professionals for medical decisions.

## 🤝 Contributing

Contributions are welcome! Please:

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Follow PEP 8 style guidelines

## 📖 Documentation

- [AGENT_BEHAVIOR.md](AGENT_BEHAVIOR.md) - Detailed documentation on anti-hallucination mechanisms
- [chainlit.md](chainlit.md) - About page shown in the UI
- [FHIR Documentation](https://www.hl7.org/fhir/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Chainlit Docs](https://docs.chainlit.io/)

## License

MIT License - feel free to use for your projects!

## Support

For issues or questions:
- Check the FHIR API documentation: https://www.hl7.org/fhir/
- LangGraph docs: https://langchain-ai.github.io/langgraph/
- Chainlit docs: https://docs.chainlit.io/
- HAPI FHIR Server: https://hapi.fhir.org/

---

Built with ❤️ using LangGraph, OpenAI, and FHIR
