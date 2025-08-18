# A2A Protocol Showcase Setup Guide

This guide will help you set up and run the complete A2A protocol demonstration with three components:

1. **Parent Agent** (existing A2A server) - Complex capabilities
2. **Client Backend** (FastAPI + LangGraph) - Simple capabilities + A2A routing  
3. **Frontend** (React + Vite) - User interface

## Architecture Overview

```
React Frontend (:3000)
    ↓ HTTP API calls
FastAPI Client Backend (:8000) 
    ↓ A2A Protocol
Parent A2A Agent (:8181)
```

## Prerequisites

- Python 3.12+
- Node.js 18+ 
- uv package manager
- Your existing A2A agent working

## Setup Instructions

### 1. Start Parent A2A Agent (Port 8181)

First, ensure your existing A2A agent is running:

```bash
# In the main project directory
uv run python -m app --host 0.0.0.0 --port 8181
```

Verify it's working by checking the agent card:
```bash
curl http://localhost:8181/.well-known/agent_card
```

### 2. Setup Client Backend (Port 8000)

```bash
cd client_backend

# Install dependencies
uv sync

# Copy environment file (optional - uses defaults)
cp .env.example .env

# Start the client backend
uv run python run.py
```

The client backend will:
- Connect to your parent agent via A2A protocol
- Fetch the parent's agent card
- Start serving on http://localhost:8000

### 3. Setup Frontend (Port 3000)

```bash
cd client

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at http://localhost:3000

## Testing the A2A Showcase

### 1. Agent Discovery
- Visit http://localhost:3000
- See side-by-side comparison of Client vs Parent agent capabilities
- Notice how each agent advertises different skills

### 2. Intelligent Routing
Try these example queries to see routing in action:

**Local Processing (Client Agent):**
- "Hello world"
- "What is 15 * 23?"
- "Make this text UPPERCASE"
- "What time is it?"

**A2A Delegation (Parent Agent):**
- "Find recent papers on transformer architectures"
- "What are the latest developments in AI?"
- "Search for information about machine learning"

### 3. Multi-Turn Conversations
- Use the conversation interface
- See how context is preserved across agent boundaries
- Watch routing decisions for each message

## API Testing (Optional)

Test the client backend directly:

```bash
# Local hello world
curl -X POST http://localhost:8000/hello

# Get routing decision
curl -X POST http://localhost:8000/routing-decision \
  -H "Content-Type: application/json" \
  -d '{"query": "Find AI research papers"}'

# Process query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is 7 * 8?"}'

# Agent cards
curl http://localhost:8000/agent-cards
```

## What This Demonstrates

### A2A Protocol Benefits

1. **Agent Discovery**: Automatic capability discovery via agent cards
2. **Intelligent Routing**: Tasks routed based on agent specialization  
3. **Standardized Communication**: Same protocol works across different agents
4. **Graceful Fallback**: Local processing when A2A communication fails
5. **Context Preservation**: Multi-turn conversations across agent boundaries
6. **Scalable Architecture**: Easy to add more specialized agents

### Real-World Applications

- **Microservices for AI**: Different models/agents for different tasks
- **Federated AI**: Multiple organizations' agents working together  
- **Specialized Agents**: Research agent + writing agent + data agent
- **Load Balancing**: Route to available agents
- **Cost Optimization**: Cheap agents for simple tasks, expensive for complex

## Troubleshooting

### Parent Agent Connection Issues
```bash
# Check if parent agent is running
curl http://localhost:8181/.well-known/agent_card

# Check client backend logs
uv run python main.py  # Look for A2A connection messages
```

### Frontend Build Issues
```bash
cd client
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Port Conflicts
- Parent Agent: 8181 (configurable in your main app)
- Client Backend: 8000 (change in main.py)
- Frontend: 3000 (change with --port flag)

## Project Structure

```
15_A2A_LangGraph/
├── app/                    # Your existing parent agent
├── client_backend/         # FastAPI client with LangGraph
│   ├── main.py            # FastAPI app
│   ├── graph.py           # LangGraph with routing
│   ├── a2a_integration.py # A2A protocol client
│   ├── local_capabilities.py # Local processing
│   └── models.py          # Pydantic models
├── client/                # React frontend
│   ├── src/components/    # UI components
│   ├── src/services/      # API integration
│   └── src/types/         # TypeScript types
└── A2A_CLIENT_SETUP.md   # This guide
```

## Next Steps

1. **Extend Local Capabilities**: Add more client agent skills
2. **Add More Agents**: Create specialized agents for different domains
3. **Implement Authentication**: Add API keys and authentication
4. **Add Monitoring**: Track routing decisions and performance
5. **Deploy**: Deploy each component independently

This showcase demonstrates the power of the A2A protocol for building modular, scalable AI agent architectures!