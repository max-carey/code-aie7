# A2A Protocol Complete Guide & Demo

A comprehensive demonstration of the Agent-to-Agent (A2A) protocol with intelligent routing, real-time communication, and a modern React frontend.

## 🚀 Quick Start - Get All Three Processes Running

### Prerequisites
- Python 3.12+
- Node.js 18+ 
- uv package manager
- OpenAI API key
- Tavily API key (optional, for web search)

### 1. Environment Setup

```bash
# Create .env file in the root directory
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
TOOL_LLM_NAME=gpt-4o-mini
TOOL_LLM_URL=https://api.openai.com/v1
RAG_DATA_DIR=data
OPENAI_CHAT_MODEL=gpt-4o-mini
EOF
```

### 2. Start All Three Processes

**Terminal 1 - Parent A2A Agent (Port 8181):**
```bash
# Install dependencies
uv sync

# Start the parent A2A agent server
uv run python -m app --host 0.0.0.0 --port 8181
```

**Terminal 2 - Client Backend (Port 8000):**
```bash
cd client_backend

# Install dependencies
uv sync

# Start the client backend
uv run python run.py
```

**Terminal 3 - React Frontend (Port 5173):**
```bash
cd client

# Install dependencies
npm install

# Start the frontend
npm run dev
```

### 3. Verify Everything is Running

- **Parent Agent**: http://localhost:8181/.well-known/agent-card.json
- **Client Backend**: http://localhost:8000/health
- **Frontend Demo**: http://localhost:5173/

## 🏗️ Architecture Overview

```
React Frontend (:5173)
    ↓ HTTP API calls
FastAPI Client Backend (:8000) 
    ↓ A2A Protocol JSON-RPC
Parent A2A Agent (:8181)
    ↓ Tool calls
External APIs (OpenAI, Tavily, ArXiv)
```

### Component Responsibilities

**🌐 Parent A2A Agent** (Complex Capabilities):
- Web search via Tavily
- Academic paper search via ArXiv  
- Document retrieval (RAG)
- Advanced reasoning with GPT-4

**🏠 Client Backend** (Simple Capabilities + Routing):
- Basic math calculations
- Text processing (uppercase, word count)
- Hello world greetings
- Intelligent routing decisions
- A2A protocol communication

**⚛️ React Frontend** (User Interface):
- Agent capability comparison
- Intelligent routing demonstration
- Multi-turn conversations
- Real-time response display

## 🎯 What This Demonstrates

### A2A Protocol Core Features

1. **🔍 Agent Discovery**
   - Automatic capability discovery via agent cards
   - Dynamic skill advertisement
   - Protocol version negotiation

2. **🧠 Intelligent Routing**
   - Query analysis and capability matching
   - Confidence-based routing decisions
   - Fallback to local processing

3. **📡 Standardized Communication**
   - JSON-RPC 2.0 protocol
   - Structured message formats
   - Task and context management

4. **🔄 Real-time Interaction**
   - Streaming responses
   - Status updates during processing
   - Multi-turn conversation support

5. **⚡ Graceful Degradation**
   - Fallback when A2A communication fails
   - Local processing capabilities
   - Error handling and recovery

## 🧪 Testing the Demo

### Intelligent Routing Examples

**Local Processing (Client Agent):**
- ✅ "Hello world" → Client (greeting capability)
- ✅ "What is 15 * 23?" → Client (math capability)  
- ✅ "Make this text UPPERCASE" → Client (text processing)
- ✅ "What time is it?" → Client (timestamp capability)

**A2A Delegation (Parent Agent):**
- 🌐 "Find recent papers on transformer architectures" → Parent (ArXiv search)
- 🌐 "What are the latest developments in AI?" → Parent (web search)
- 🌐 "Search for information about machine learning" → Parent (web search)
- 🌐 "Analyze documents about policy" → Parent (RAG retrieval)

### Multi-Turn Conversation Testing

1. Start with: "Hello! Can you help me with research?"
2. Follow up: "Find papers on machine learning"  
3. Continue: "What's 25 * 16?" (switches to local)
4. Then: "Search for latest AI news" (back to parent)
5. Finally: "Can you summarize what we've discussed?"

## 📊 Performance & Response Analysis

### Typical Response Times
- **Local Processing**: 50-200ms (immediate calculations)
- **A2A Web Search**: 3-8 seconds (Tavily + GPT processing)
- **A2A ArXiv Search**: 5-12 seconds (ArXiv API + analysis)
- **A2A Document Retrieval**: 2-5 seconds (vector search + generation)

### Response Quality
- **Real-time Information**: Current 2024 AI developments, recent papers
- **Accurate Results**: Proper academic citations, verified web sources
- **Context Preservation**: Multi-turn conversations maintain state
- **Structured Output**: Clean formatting, proper error handling

## 🔧 API Reference

### Client Backend Endpoints

```bash
# Health check
GET /health

# Agent capabilities comparison
GET /agent-cards

# Local hello world (always client)
POST /hello

# Get routing decision only
POST /routing-decision
{
  "query": "Find recent AI papers"
}

# Full query processing with routing
POST /query
{
  "query": "What is 7 * 8?"
}

# Multi-turn conversation
POST /chat
{
  "message": "Hello!",
  "conversation_id": "conv_123"
}
```

### A2A Protocol Messages

**Agent Card Resolution:**
```bash
GET /.well-known/agent-card.json
```

**Task Submission:**
```json
{
  "jsonrpc": "2.0",
  "method": "task.submit",
  "params": {
    "message": {
      "role": "user",
      "parts": [{"kind": "text", "text": "Find AI papers"}],
      "message_id": "msg_123"
    }
  },
  "id": "req_456"
}
```

## 💻 Key Code Architecture Analysis

### Client Agent as Independent LangGraph Agent

The client backend demonstrates a **fully autonomous agent** built with FastAPI and LangGraph that can operate independently AND communicate with other agents via A2A protocol.

#### 1. Client Agent Core Structure (`client_backend/a2a_client_backend/graph.py`)

```python
class ClientAgentState(TypedDict):
    """State schema for client agent graph"""
    query: str
    response: str
    agent_source: str  # "client" or "parent"
    routing_decision: str
    routing_reason: str
    route_to: str      # "client" or "parent" - for routing decisions
    reason: str        # reason for routing decision
    confidence: float
    execution_time: int
    conversation_id: str
    chat_mode: bool
    force_local: bool
    routing_only: bool
    timestamp: datetime

def build_client_agent_graph(a2a_integration: A2AIntegration):
    """Build the client agent LangGraph with routing capabilities"""
    
    async def capability_router(state: ClientAgentState) -> Dict[str, Any]:
        """🧠 THE BRAIN: Determines whether to handle locally or route to parent"""
        query = state["query"]
        
        # 🏠 LOCAL PROCESSING: Handle simple tasks locally
        local_capability = determine_local_capability(query)
        
        if local_capability and not has_complex_indicators(query):
            return local_processor(state)  # ✅ Handle locally
        
        # 🌐 A2A DELEGATION: Route complex tasks to parent agent
        return await a2a_delegate(state)   # ✅ Call parent via A2A
    
    # 🔗 Build the LangGraph
    workflow = StateGraph(ClientAgentState)
    workflow.add_node("capability_router", capability_router)
    workflow.set_entry_point("capability_router")
    workflow.add_edge("capability_router", END)
    
    return workflow.compile()
```

#### 2. Local Agent Capabilities (`client_backend/a2a_client_backend/local_capabilities.py`)

```python
def determine_local_capability(query: str) -> str:
    """🏠 Client Agent's OWN capabilities - what it can do without help"""
    query_lower = query.lower()
    
    # ✅ MATH: Simple calculations
    if any(op in query for op in ['+', '-', '*', '/', 'calculate', 'math']):
        return "basic_math"
    
    # ✅ GREETINGS: Hello world generation  
    if any(word in query_lower for word in ['hello', 'hi', 'greeting']):
        return "hello_world"
    
    # ✅ TEXT PROCESSING: String manipulations
    if any(word in query_lower for word in ['uppercase', 'lowercase', 'count']):
        return "text_processing"
    
    # ❌ NOT LOCAL: Complex tasks need parent agent
    return None

def process_locally(query: str) -> Dict[str, Any]:
    """🏠 Client Agent processing - runs entirely locally"""
    start_time = time.time()
    
    capability = determine_local_capability(query)
    
    if capability == "basic_math":
        # 🧮 Client agent does its own math
        result = eval_math_expression(query)
        return {
            "response": f"🧮 **Local Calculation**: {result}",
            "capability_used": "basic_math",
            "execution_time": int((time.time() - start_time) * 1000)
        }
    
    elif capability == "hello_world":
        # 👋 Client agent generates its own greetings
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {
            "response": f"👋 **Hello from Client Agent!** Generated at {timestamp}",
            "capability_used": "hello_world", 
            "execution_time": int((time.time() - start_time) * 1000)
        }
    
    # ... more local capabilities
```

#### 3. A2A Communication Layer (`client_backend/a2a_client_backend/a2a_integration.py`)

```python
class A2AIntegration:
    """🌐 A2A Protocol Client - How client agent talks to parent agent"""
    
    async def send_message_to_parent(self, message: str, context_id: Optional[str] = None):
        """🚀 CLIENT → PARENT: Send message via A2A protocol"""
        
        # 📦 Prepare A2A message payload
        send_message_payload = {
            'message': {
                'role': 'user',
                'parts': [{'kind': 'text', 'text': message}],
                'message_id': uuid4().hex,
            }
        }
        
        # 🔗 Add conversation context for multi-turn chats
        if context_id:
            send_message_payload['message']['context_id'] = context_id
        
        # 📡 Create JSON-RPC request
        request = SendMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(**send_message_payload)
        )
        
        logger.info(f"🌐 Sending message to parent agent: {message[:100]}...")
        
        # 🚀 ACTUAL A2A PROTOCOL CALL
        response = await self.client.send_message(request)
        
        # 📥 Extract clean response content
        result = response.model_dump(mode='json', exclude_none=True)
        return self._extract_response_content(result)
```

#### 4. The Routing Decision Logic (`client_backend/a2a_client_backend/graph.py`)

```python
async def a2a_delegate(state: ClientAgentState) -> Dict[str, Any]:
    """🌐 DELEGATE TO PARENT: When client agent needs help"""
    start_time = time.time()
    
    try:
        logger.info(f"🌐 CLIENT AGENT: Delegating to parent agent via A2A...")
        
        # 🚀 MAKE THE A2A CALL
        result = await a2a_integration.send_message_to_parent(
            state["query"],
            context_id=state.get("conversation_id")
        )
        
        execution_time = int((time.time() - start_time) * 1000)
        
        # ✅ SUCCESS: Parent agent handled the request
        return {
            "response": result["content"],
            "agent_source": "parent",  # 🌐 Came from parent agent
            "routing_decision": "Delegated to Parent Agent via A2A protocol",
            "routing_reason": "Query requires specialized capabilities",
            "confidence": 0.8,
            "execution_time": execution_time,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"❌ A2A delegation failed: {e}")
        
        # 🔄 FALLBACK: Try to handle locally if A2A fails
        try:
            fallback_result = process_locally(state["query"])
            fallback_response = f"⚠️ A2A Communication Failed - Processed Locally\n\n{fallback_result['response']}"
            
            return {
                "response": fallback_response,
                "agent_source": "client",  # 🏠 Fallback to local
                "routing_decision": "A2A failed, fallback to local processing",
                "routing_reason": f"A2A error: {str(e)}",
                "confidence": 0.3,
                "execution_time": execution_time,
                "timestamp": datetime.now()
            }
        except Exception as fallback_error:
            # 💥 Complete failure
            return {"response": f"Error: Both A2A and local fallback failed"}
```

#### 5. FastAPI Integration (`client_backend/a2a_client_backend/main.py`)

```python
app = FastAPI(title="A2A Client Backend", version="0.1.0")

# 🌍 Global LangGraph instance - THIS IS THE CLIENT AGENT
client_graph = None
a2a_integration = None

@app.on_event("startup")
async def startup_event():
    """🚀 Initialize the client agent on startup"""
    global client_graph, a2a_integration
    
    # 🔗 Connect to parent agent via A2A
    a2a_integration = A2AIntegration()
    await a2a_integration.initialize()
    
    # 🧠 Build the client agent LangGraph
    client_graph = build_client_agent_graph(a2a_integration)
    
    logger.info("✅ Client Agent initialized and connected to parent!")

@app.post("/query", response_model=TaskResponse)
async def process_query(request: QueryRequest):
    """🎯 MAIN ENDPOINT: Client agent processes any query"""
    
    # 🧠 RUN THE CLIENT AGENT (LangGraph execution)
    result = await client_graph.ainvoke({
        "query": request.query
    })
    
    # 📤 Return response (could be from client OR parent agent)
    return TaskResponse(
        content=result["response"],
        agent_source=result["agent_source"],  # 🏠 "client" or 🌐 "parent"
        routing_decision=result.get("routing_decision"),
        execution_time=result.get("execution_time", 0)
    )

@app.post("/routing-decision", response_model=RoutingDecision)
async def get_routing_decision(request: QueryRequest):
    """🎯 ROUTING PREVIEW: See where query would go without executing"""
    
    # 🧠 Ask client agent for routing decision only
    result = await client_graph.ainvoke({
        "query": request.query,
        "routing_only": True  # 🔍 Just decide, don't execute
    })
    
    return RoutingDecision(
        route_to=result["route_to"],      # 🏠 "client" or 🌐 "parent" 
        reason=result["reason"],          # 📝 Why this decision
        confidence=result["confidence"]   # 📊 How confident (0.0-1.0)
    )
```

### 🔄 Complete Request Flow Example

Here's what happens when a user asks **"Find recent papers on AI"**:

```python
# 1. 📥 REQUEST ARRIVES
POST /query {"query": "Find recent papers on AI"}

# 2. 🧠 CLIENT AGENT ANALYZES
capability_router(state) {
    query = "Find recent papers on AI"
    local_capability = determine_local_capability(query)  # ❌ None (not local)
    
    complex_indicators = ['research', 'papers', 'find']   # ✅ Found!
    has_complex_indicator = True
    
    # 🌐 DECISION: Route to parent agent
    return await a2a_delegate(state)
}

# 3. 🚀 A2A PROTOCOL CALL
a2a_delegate(state) {
    # 📡 Send JSON-RPC request to parent agent
    await a2a_integration.send_message_to_parent("Find recent papers on AI")
}

# 4. 🌐 PARENT AGENT PROCESSES
Parent Agent:
- Uses ArXiv tool to search academic papers
- Finds real papers with titles, authors, dates
- Formats response with structured information

# 5. 📥 PARENT RESPONSE RECEIVED
{
  "content": "Here are recent papers on AI:\n1. 'Attention Is All You Need'...",
  "task_id": "123",
  "status": "completed"
}

# 6. 📤 CLIENT AGENT RETURNS RESULT
{
  "content": "Here are recent papers on AI...",
  "agent_source": "parent",           # 🌐 Came from parent
  "routing_decision": "Delegated to Parent Agent via A2A protocol",
  "execution_time": 8602             # 8.6 seconds for research
}
```

### 🏠 vs 🌐 Comparison: Local vs A2A Processing

| Feature | 🏠 Local Processing (Client Agent) | 🌐 A2A Processing (Parent Agent) |
|---------|-----------------------------------|-----------------------------------|
| **Capabilities** | Math, greetings, text processing | Web search, ArXiv, RAG, complex reasoning |
| **Speed** | 50-200ms (instant) | 3-12 seconds (external APIs) |
| **Dependencies** | None (fully local) | Requires parent agent connection |
| **Fallback** | Always available | Falls back to local if A2A fails |
| **Example Queries** | "What is 5+3?", "Hello world" | "Find AI papers", "Latest tech news" |

### 🎯 Key Architectural Benefits

1. **🧠 Client Agent is a Real Agent**: Built with LangGraph, has its own capabilities, makes intelligent decisions
2. **🌐 A2A as Enhancement**: Parent agent extends capabilities without replacing local ones  
3. **🔄 Intelligent Routing**: Automatic decision-making about local vs. remote processing
4. **⚡ Graceful Fallback**: System continues working even if A2A communication fails
5. **📡 Standard Protocol**: Uses JSON-RPC A2A protocol for reliable agent-to-agent communication

This demonstrates how A2A enables **hierarchical agent architectures** where smaller, specialized agents can leverage larger, more capable agents while maintaining their own autonomy and local processing abilities! 🚀

## 🛠️ Development Guide

### Project Structure

```
15_A2A_LangGraph/
├── app/                           # Parent A2A Agent
│   ├── __main__.py               # Server entry point  
│   ├── agent.py                  # Core agent logic
│   ├── agent_executor.py         # Task execution
│   ├── tools.py                  # Tavily, ArXiv, RAG tools
│   ├── rag.py                    # Document retrieval
│   └── test_client.py            # A2A protocol test
├── client_backend/               # FastAPI Client Backend
│   ├── a2a_client_backend/
│   │   ├── main.py              # FastAPI app
│   │   ├── graph.py             # LangGraph routing
│   │   ├── a2a_integration.py   # A2A client
│   │   ├── local_capabilities.py # Local processing
│   │   └── models.py            # Pydantic schemas
│   └── run.py                   # Entry point
├── client/                      # React Frontend
│   ├── src/
│   │   ├── components/          # UI components
│   │   ├── services/            # API integration
│   │   ├── types/               # TypeScript types
│   │   └── App.tsx              # Main application
│   ├── package.json
│   └── vite.config.ts
└── data/                        # RAG documents
```

### Adding New Capabilities

**Extend Local Capabilities:**
```python
# In client_backend/a2a_client_backend/local_capabilities.py
def determine_local_capability(query: str) -> str:
    # Add new capability detection
    if "weather" in query.lower():
        return "weather_info"
    # ... existing logic
```

**Add New A2A Skills:**
```python
# In app/__main__.py
skills = [
    AgentSkill(
        id='new_skill',
        name='New Capability',
        description='Description of what it does',
        tags=['tag1', 'tag2'],
        examples=['Example query'],
    ),
    # ... existing skills
]
```

### Configuration Options

**Environment Variables:**
```bash
# Required
OPENAI_API_KEY=your_key
TAVILY_API_KEY=your_key

# Optional with defaults
TOOL_LLM_NAME=gpt-4o-mini
TOOL_LLM_URL=https://api.openai.com/v1
RAG_DATA_DIR=data
OPENAI_CHAT_MODEL=gpt-4o-mini

# Development
LANGCHAIN_VERBOSE=true           # Debug tool execution
```

**Port Configuration:**
- Parent Agent: `--port 8181` (configurable)
- Client Backend: Port 8000 (change in `run.py`)
- Frontend: `--port 5173` (Vite default)

## 🧪 Protocol Verification

✅ **A2A Communication Flow**: Agent discovery → Task submission → Real-time updates → Structured response → Context preservation

**Example Response Structure**:
```json
{
  "result": {
    "artifacts": [{"parts": [{"text": "Here are recent papers..."}]}],
    "contextId": "ctx_789",
    "status": {"state": "completed"}
  }
}
```

## 🚀 Real-World Applications

### Enterprise Use Cases

1. **🏢 Microservices for AI**
   - Different models for different tasks
   - Cost optimization (cheap vs. expensive models)
   - Specialized expertise per service

2. **🤝 Federated AI Systems**
   - Multiple organizations' agents collaborating
   - Secure, standardized communication
   - Capability sharing without data sharing

3. **⚖️ Load Balancing & Scaling**
   - Route to available agents
   - Horizontal scaling of AI capabilities
   - Graceful degradation under load

4. **🎯 Specialized Agent Networks**
   - Research agent + Writing agent + Data agent
   - Domain expertise distribution
   - Complex multi-step workflows

## 🔍 Need Help?

**📋 For troubleshooting, debugging, and detailed solutions, see:**
👉 **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** - Comprehensive troubleshooting guide

Quick checks:
- ✅ All three services running: `curl http://localhost:8181/.well-known/agent-card.json && curl http://localhost:8000/health && curl http://localhost:5173/`
- ✅ Environment variables set: `echo $OPENAI_API_KEY $TAVILY_API_KEY`
- ✅ Correct startup order: Parent Agent → Client Backend → Frontend

## 🎉 Success Indicators

When everything is working correctly, you should see:

1. ✅ **Agent Card Discovery**: Client backend logs "Successfully connected to parent agent"
2. ✅ **Intelligent Routing**: Different queries go to appropriate agents
3. ✅ **Real Research Results**: ArXiv papers with real titles, authors, dates
4. ✅ **Clean Formatting**: No raw JSON in frontend responses
5. ✅ **Multi-turn Context**: Conversations maintain state across messages
6. ✅ **Graceful Fallback**: Local processing when A2A fails

This implementation demonstrates the full power of the A2A protocol for building modular, scalable, and intelligent AI agent architectures! 🚀

---

## 📚 Additional Resources

- **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** - Comprehensive debugging guide
- **[CLAUDE.md](./CLAUDE.md)** - Development commands reference