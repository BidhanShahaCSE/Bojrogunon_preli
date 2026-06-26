# QueueStorm Investigator API

AI-powered investigation API for the QueueStorm Investigator hackathon challenge.

## Architecture

This project implements a complete, modular, and production-ready investigation API using a layered architecture.

```
app/
  api/          # FastAPI routers
  graph/        # LangGraph workflow and state
  nodes/        # LangGraph nodes (reasoning stages)
  llms/         # LLM client factory
  prompts/      # LangChain Prompt templates
  schemas/      # Pydantic schemas
  services/     # Core business logic
  utils/        # Utility functions (logging, JSON parsing)
  tests/        # Pytest test suite
```

### LangGraph Workflow

The reasoning pipeline is built as an 11-node LangGraph workflow:
1. `intake` -> 2. `complaint_understanding` -> 3. `transaction_matcher` -> 4. `evidence_reasoner` -> 5. `classifier` -> 6. `severity` -> 7. `department_router` -> 8. `agent_summary` -> 9. `customer_reply` -> 10. `safety_guard` -> 11. `confidence` -> 12. `final_response`

Each node maintains and updates a central `GraphState`. This ensures a logical progression of reasoning, where each step utilizes the specialized `llama-3.3-70b-versatile` model via the Groq API.

## Requirements

- Python 3.12+
- `uv` (recommended) or `pip`
- Docker (optional)

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and set your GROQ_API_KEY
   ```

## Running the Application

### Locally
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### With Docker
```bash
docker-compose up --build
```

## Testing

```bash
pytest app/tests/
```

## Design Decisions

- **Multi-LLM Strategy**: Instead of one massive prompt, we use specialized prompts for extraction, matching, reasoning, routing, drafting, and safety checking. This improves accuracy and robustness.
- **Safety**: A dedicated `safety_guard` node is the last LLM step. It acts as a strict verification layer against PII requests (PIN, OTP), false promises (Refunds), and prompt injections.
- **Error Handling**: Graceful fallback values are implemented for LLM parsing failures, returning safe defaults rather than crashing.

## API Examples

### `GET /health`
```bash
curl -X GET http://localhost:8000/health
```

### `POST /analyze-ticket`
```bash
curl -X POST http://localhost:8000/analyze-ticket \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "T-001",
    "complaint": "I was charged twice for my Netflix subscription.",
    "language": "en",
    "channel": "in_app_chat",
    "user_type": "customer",
    "transaction_history": [
      {
        "transaction_id": "TX-1",
        "timestamp": "2023-10-01T12:00:00Z",
        "type": "payment",
        "amount": 15.99,
        "counterparty": "Netflix",
        "status": "completed"
      }
    ]
  }'
```
