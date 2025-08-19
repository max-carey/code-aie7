# A2A Protocol Quick Start Guide

A simple 3-component Agent-to-Agent system with intelligent routing.

## 🏗️ Architecture

```
React Frontend (5174) ← → FastAPI Client (8001) ← → A2A Parent Agent (8181)
```

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Create .env file
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
EOF
```

### 2. Start All Three Services

**Terminal 1 - A2A Parent Agent:**
```bash
uv sync
uv run python -m app --host 0.0.0.0 --port 8181
```

**Terminal 2 - Client Backend:**
```bash
cd client_backend
uv run uvicorn a2a_client_backend.main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 3 - React Frontend:**
```bash
cd client
npm install
npm run dev
```

### 3. Access the Web UI
Open: **http://localhost:5174**

## 🎯 What Each Component Does

### 🤖 A2A Parent Agent (Port 8181)
- **Purpose**: Advanced AI agent with specialized tools
- **Capabilities**: Web search, academic papers, document retrieval
- **Protocol**: Serves A2A-compliant API with AgentCard

### ⚡ Client Backend (Port 8001)  
- **Purpose**: Local agent with basic capabilities + A2A routing
- **Capabilities**: Simple math, greetings, text processing
- **Intelligence**: Decides when to handle locally vs route to parent

### 🌐 React Frontend (Port 5174)
- **Purpose**: Web interface for testing A2A protocol
- **Features**: Agent comparison, task routing demo, multi-turn chat

## 🔄 How A2A Protocol Works

1. **Discovery**: Client fetches parent's AgentCard to learn capabilities
2. **Routing**: Client decides local vs remote based on task complexity
3. **Communication**: Uses standardized JSON-RPC for agent-to-agent calls
4. **Response**: User sees seamless experience regardless of which agent responds

## ✅ Success Indicators

- Parent Agent: `"A2A Client Backend initialized successfully"`
- Client Backend: `"Successfully connected to parent agent"`
- Frontend: Agent cards displayed + interactive buttons working

## 🧪 Test the System

1. **Local Hello**: Should route to Client Agent
2. **Latest AI Research**: Should route to Parent Agent (ArXiv)  
3. **Simple Math**: Should route to Client Agent
4. **Web Search**: Should route to Parent Agent (Tavily)

## 📊 Key Benefits Demonstrated

- **Automatic Capability Discovery**: No hardcoded integrations
- **Intelligent Routing**: Tasks go to the most appropriate agent
- **Standardized Protocol**: Same interface across different agents
- **Seamless UX**: Users don't need to know which agent responds