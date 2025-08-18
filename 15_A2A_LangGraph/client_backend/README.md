# A2A Client Backend

FastAPI backend demonstrating Agent-to-Agent (A2A) communication with intelligent routing.

## Architecture

This client agent demonstrates the A2A protocol by:

1. **Local Capabilities**: Handles simple tasks (math, text processing, timestamps)
2. **Intelligent Routing**: Decides whether to process locally or delegate via A2A
3. **A2A Communication**: Routes complex tasks to the parent agent
4. **Fallback Handling**: Graceful degradation when A2A communication fails

## Setup

```bash
# Install dependencies
uv sync

# Copy environment file
cp .env.example .env

# Start the server
uv run python run.py

# Or using the module directly
uv run python -m a2a_client_backend.main
```

The server will run on `http://localhost:8000`

## API Endpoints

- `GET /agent-cards` - Get both client and parent agent capabilities
- `POST /hello` - Local hello world (always client agent)
- `POST /routing-decision` - Get routing decision without execution
- `POST /query` - Process query with intelligent routing
- `POST /chat` - Multi-turn conversation with context

## LangGraph Flow

```
START → capability_router → [local_processor | a2a_delegate] → END
```

### Routing Logic

**Local Processing** (Client Agent):
- Hello world greetings
- Basic math calculations
- Text processing (uppercase, lowercase, word count)
- Timestamp operations
- System information

**A2A Delegation** (Parent Agent):
- Web search queries
- Academic paper research
- Document analysis
- Complex reasoning tasks
- Latest news/information

## A2A Protocol Benefits

1. **Capability Discovery**: Client knows parent's abilities via agent card
2. **Intelligent Routing**: Tasks go to the most appropriate agent
3. **Standardized Communication**: Same protocol across different agents
4. **Graceful Fallback**: Local processing when A2A fails
5. **Context Preservation**: Multi-turn conversations work across agents

## Testing

Ensure your parent A2A agent is running on port 8181:

```bash
# In the main project directory
uv run python -m app --host 0.0.0.0 --port 8181
```

Then start this client backend:

```bash
uv run python main.py
```

Test with curl:

```bash
# Local processing
curl -X POST http://localhost:8000/hello

# Routing decision
curl -X POST http://localhost:8000/routing-decision \
  -H "Content-Type: application/json" \
  -d '{"query": "Find recent AI papers"}'

# Full query processing
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is 5 + 3?"}'
```