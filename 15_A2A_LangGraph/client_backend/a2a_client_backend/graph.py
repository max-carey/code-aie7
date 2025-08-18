import logging
import time
from datetime import datetime
from typing import Dict, Any, Annotated, TypedDict, List

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage

from .a2a_integration import A2AIntegration
from .local_capabilities import process_locally, determine_local_capability

logger = logging.getLogger(__name__)

class ClientAgentState(TypedDict):
    """State schema for client agent graph"""
    query: str
    response: str
    agent_source: str  # "client" or "parent"
    routing_decision: str
    routing_reason: str
    route_to: str  # "client" or "parent" - for routing decisions
    reason: str   # reason for routing decision
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
        """Determine whether to handle locally or route to parent agent"""
        query = state["query"]
        
        # Handle special routing modes
        if state.get("force_local"):
            # For force local, we process immediately
            return local_processor(state)
        
        if state.get("routing_only"):
            # For routing only, return just the routing decision
            return routing_decision_only(state)
        
        # For normal processing, determine the route and process
        local_capability = determine_local_capability(query)
        
        # Check if we can handle it locally
        if local_capability:
            confidence = 0.9  # High confidence for clearly local tasks
            
            # But check for complexity indicators that might need parent
            complex_indicators = [
                'research', 'papers', 'arxiv', 'search', 'web', 'internet',
                'latest', 'recent', 'news', 'find', 'analyze documents',
                'rag', 'retrieval', 'database', 'compare', 'versus'
            ]
            
            query_lower = query.lower()
            has_complex_indicator = any(indicator in query_lower for indicator in complex_indicators)
            
            if has_complex_indicator:
                confidence = 0.3  # Lower confidence, likely needs parent
                return await a2a_delegate(state)
            else:
                return local_processor(state)
        
        # No clear local capability, route to parent
        return await a2a_delegate(state)
    
    def routing_decision_only(state: ClientAgentState) -> Dict[str, Any]:
        """Return routing decision without executing"""
        query = state["query"]
        local_capability = determine_local_capability(query)
        
        complex_indicators = [
            'research', 'papers', 'arxiv', 'search', 'web', 'internet',
            'latest', 'recent', 'news', 'find', 'analyze documents',
            'rag', 'retrieval', 'database', 'compare', 'versus'
        ]
        
        query_lower = query.lower()
        has_complex_indicator = any(indicator in query_lower for indicator in complex_indicators)
        
        if local_capability and not has_complex_indicator:
            route_to = "client"
            reason = f"Query matches local capability: {local_capability}"
            confidence = 0.9
        else:
            route_to = "parent"
            if has_complex_indicator:
                reason = "Query requires complex capabilities (research, web search, or document analysis)"
            else:
                reason = "Query doesn't match simple local capabilities"
            confidence = 0.8 if has_complex_indicator else 0.6
        
        # Return the state with routing decision information
        return {
            "route_to": route_to,
            "reason": reason,
            "confidence": confidence,
            "timestamp": datetime.now(),
            "routing_decision": reason,
            "routing_reason": reason
        }
    
    def local_processor(state: ClientAgentState) -> Dict[str, Any]:
        """Process query using local capabilities"""
        start_time = time.time()
        
        try:
            result = process_locally(state["query"])
            
            return {
                "response": result["response"],
                "agent_source": "client",
                "routing_decision": "Processed locally by Client Agent",
                "routing_reason": f"Local capability: {result.get('capability_used', 'general')}",
                "confidence": 0.9,
                "execution_time": result["execution_time"],
                "timestamp": datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error in local processing: {e}")
            execution_time = int((time.time() - start_time) * 1000)
            
            return {
                "response": f"Error in local processing: {str(e)}",
                "agent_source": "client",
                "routing_decision": "Local processing error",
                "routing_reason": str(e),
                "confidence": 0.0,
                "execution_time": execution_time,
                "timestamp": datetime.now()
            }
    
    async def a2a_delegate(state: ClientAgentState) -> Dict[str, Any]:
        """Delegate query to parent agent via A2A protocol"""
        start_time = time.time()
        
        try:
            logger.info(f"Delegating to parent agent via A2A: {state['query'][:100]}...")
            
            # Send message to parent agent
            result = await a2a_integration.send_message_to_parent(
                state["query"],
                context_id=state.get("conversation_id")
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return {
                "response": result["content"],
                "agent_source": "parent",
                "routing_decision": "Delegated to Parent Agent via A2A protocol",
                "routing_reason": "Query requires specialized capabilities available in Parent Agent",
                "confidence": 0.8,
                "execution_time": execution_time,
                "timestamp": datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error in A2A delegation: {e}")
            execution_time = int((time.time() - start_time) * 1000)
            
            # Fallback to local processing on A2A failure
            try:
                fallback_result = process_locally(state["query"])
                fallback_response = f"⚠️ A2A Communication Failed - Processed Locally\n\n{fallback_result['response']}\n\nNote: Could not connect to Parent Agent. Error: {str(e)}"
                
                return {
                    "response": fallback_response,
                    "agent_source": "client",
                    "routing_decision": "A2A failed, fallback to local processing",
                    "routing_reason": f"A2A error: {str(e)}",
                    "confidence": 0.3,
                    "execution_time": execution_time,
                    "timestamp": datetime.now()
                }
            except Exception as fallback_error:
                return {
                    "response": f"Error: Both A2A delegation and local fallback failed. A2A Error: {str(e)}, Fallback Error: {str(fallback_error)}",
                    "agent_source": "client",
                    "routing_decision": "Complete failure",
                    "routing_reason": f"A2A and fallback errors: {str(e)}, {str(fallback_error)}",
                    "confidence": 0.0,
                    "execution_time": execution_time,
                    "timestamp": datetime.now()
                }
    
    # Build the graph
    workflow = StateGraph(ClientAgentState)
    
    # Add only the capability router node since it handles everything
    workflow.add_node("capability_router", capability_router)
    
    # Set entry point
    workflow.set_entry_point("capability_router")
    
    # Connect to end
    workflow.add_edge("capability_router", END)
    
    # Compile the graph
    app = workflow.compile()
    
    logger.info("Client Agent LangGraph compiled successfully")
    return app

async def test_graph_routing():
    """Test function to verify routing logic"""
    test_queries = [
        "Hello world",
        "What is 5 + 3?",
        "Find recent papers on AI",
        "What time is it?",
        "Search for latest news on machine learning"
    ]
    
    # This would require A2A integration to be set up
    # For now, just test the routing decisions
    for query in test_queries:
        local_cap = determine_local_capability(query)
        print(f"Query: {query}")
        print(f"Local capability: {local_cap}")
        print("---")