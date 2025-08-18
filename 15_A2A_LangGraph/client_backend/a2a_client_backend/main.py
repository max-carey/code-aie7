import logging
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import asyncio
from dotenv import load_dotenv

# Configure LangSmith tracing for Client Agent
load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "A2A-Client-Agent"

from .graph import build_client_agent_graph
from .a2a_integration import A2AIntegration
from .models import QueryRequest, ChatRequest, TaskResponse, ConversationMessage, RoutingDecision

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="A2A Client Backend", version="0.1.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
client_graph = None
a2a_integration = None

@app.on_event("startup")
async def startup_event():
    global client_graph, a2a_integration
    logger.info("Initializing A2A Client Backend...")
    
    try:
        # Initialize A2A integration
        a2a_integration = A2AIntegration()
        await a2a_integration.initialize()
        
        # Build client agent graph
        client_graph = build_client_agent_graph(a2a_integration)
        
        logger.info("A2A Client Backend initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize backend: {e}")
        raise

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "a2a-client-backend"}

@app.get("/agent-cards")
async def get_agent_cards():
    """Get both client and parent agent cards for comparison"""
    try:
        parent_card = await a2a_integration.get_parent_agent_card()
        
        # Define client agent card
        client_card = {
            "name": "Client Agent",
            "description": "Local agent with simple processing capabilities and A2A routing",
            "url": "http://localhost:8000",
            "version": "1.0.0",
            "default_input_modes": ["text"],
            "default_output_modes": ["text"],
            "capabilities": {
                "streaming": False,
                "push_notifications": False
            },
            "skills": [
                {
                    "id": "hello_world",
                    "name": "Hello World Generator",
                    "description": "Generate friendly greetings with timestamps",
                    "tags": ["greeting", "local", "simple"],
                    "examples": ["Say hello", "Generate a greeting"]
                },
                {
                    "id": "basic_math",
                    "name": "Basic Mathematics",
                    "description": "Perform simple arithmetic calculations",
                    "tags": ["math", "calculation", "local"],
                    "examples": ["What is 5 + 3?", "Calculate 15 * 7"]
                },
                {
                    "id": "text_processing",
                    "name": "Text Processing",
                    "description": "Basic text transformations and formatting",
                    "tags": ["text", "formatting", "local"],
                    "examples": ["Make this uppercase", "Count words in text"]
                },
                {
                    "id": "a2a_routing",
                    "name": "A2A Task Delegation",
                    "description": "Route complex tasks to parent agent via A2A protocol",
                    "tags": ["routing", "delegation", "a2a"],
                    "examples": ["Research papers", "Web search queries"]
                }
            ]
        }
        
        return {
            "client": client_card,
            "parent": parent_card
        }
    except Exception as e:
        logger.error(f"Error fetching agent cards: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/hello", response_model=TaskResponse)
async def hello_world():
    """Simple hello world - always handled locally"""
    try:
        result = await client_graph.ainvoke({
            "query": "hello_world",
            "force_local": True
        })
        
        return TaskResponse(
            content=result["response"],
            agent_source="client",
            routing_decision="Local processing - hello world capability",
            execution_time=result.get("execution_time", 0)
        )
    except Exception as e:
        logger.error(f"Error in hello world: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/routing-decision", response_model=RoutingDecision)
async def get_routing_decision(request: QueryRequest):
    """Get routing decision without executing the query"""
    try:
        result = await client_graph.ainvoke({
            "query": request.query,
            "routing_only": True
        })
        
        
        return RoutingDecision(
            route_to=result["route_to"],
            reason=result["reason"],
            confidence=result["confidence"]
        )
    except Exception as e:
        logger.error(f"Error getting routing decision: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=TaskResponse)
async def process_query(request: QueryRequest):
    """Process query with intelligent routing"""
    try:
        result = await client_graph.ainvoke({
            "query": request.query
        })
        
        return TaskResponse(
            content=result["response"],
            agent_source=result["agent_source"],
            routing_decision=result.get("routing_decision"),
            execution_time=result.get("execution_time", 0)
        )
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ConversationMessage)
async def chat(request: ChatRequest):
    """Multi-turn conversation with context"""
    try:
        result = await client_graph.ainvoke({
            "query": request.message,
            "conversation_id": request.conversation_id,
            "chat_mode": True
        })
        
        return ConversationMessage(
            id=f"msg_{int(asyncio.get_event_loop().time() * 1000)}",
            role="assistant",
            content=result["response"],
            timestamp=result.get("timestamp"),
            agent_source=result["agent_source"],
            routing_info={
                "decision": result.get("routing_decision", ""),
                "reason": result.get("routing_reason", "")
            }
        )
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )