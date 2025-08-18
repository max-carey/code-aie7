from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class QueryRequest(BaseModel):
    query: str

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class TaskResponse(BaseModel):
    content: str
    agent_source: str  # "client" or "parent"
    routing_decision: Optional[str] = None
    execution_time: Optional[int] = None

class RoutingInfo(BaseModel):
    decision: str
    reason: str

class ConversationMessage(BaseModel):
    id: str
    role: str
    content: str
    timestamp: datetime
    agent_source: Optional[str] = None
    routing_info: Optional[RoutingInfo] = None

class RoutingDecision(BaseModel):
    route_to: str  # "client" or "parent"
    reason: str
    confidence: float