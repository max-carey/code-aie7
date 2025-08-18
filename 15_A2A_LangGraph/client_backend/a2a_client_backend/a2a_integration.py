import logging
from typing import Dict, Any, Optional
from uuid import uuid4
import httpx

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,
    MessageSendParams,
    SendMessageRequest,
)

logger = logging.getLogger(__name__)

class A2AIntegration:
    """Integration layer for communicating with the parent A2A agent"""
    
    def __init__(self, parent_base_url: str = "http://localhost:8181"):
        self.parent_base_url = parent_base_url
        self.httpx_client = None
        self.resolver = None
        self.client = None
        self.parent_agent_card = None
        
    async def initialize(self):
        """Initialize A2A client connection"""
        try:
            # Create HTTP client with extended timeout for LLM responses
            self.httpx_client = httpx.AsyncClient(timeout=httpx.Timeout(60.0))
            
            # Initialize A2A card resolver
            self.resolver = A2ACardResolver(
                httpx_client=self.httpx_client,
                base_url=self.parent_base_url,
            )
            
            # Fetch parent agent card
            logger.info(f"Fetching parent agent card from: {self.parent_base_url}")
            self.parent_agent_card = await self.resolver.get_agent_card()
            logger.info(f"Successfully connected to parent agent: {self.parent_agent_card.name}")
            
            # Initialize A2A client
            self.client = A2AClient(
                httpx_client=self.httpx_client,
                agent_card=self.parent_agent_card
            )
            
            logger.info("A2A integration initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize A2A integration: {e}")
            raise
    
    async def get_parent_agent_card(self) -> Dict[str, Any]:
        """Get parent agent card as dictionary"""
        if not self.parent_agent_card:
            raise Exception("A2A integration not initialized")
        
        return self.parent_agent_card.model_dump(exclude_none=True)
    
    async def send_message_to_parent(self, message: str, context_id: Optional[str] = None) -> Dict[str, Any]:
        """Send message to parent agent via A2A protocol"""
        if not self.client:
            raise Exception("A2A client not initialized")
        
        try:
            # Prepare message payload
            send_message_payload = {
                'message': {
                    'role': 'user',
                    'parts': [
                        {'kind': 'text', 'text': message}
                    ],
                    'message_id': uuid4().hex,
                }
            }
            
            # Add context if provided (for multi-turn conversations)
            if context_id:
                send_message_payload['message']['context_id'] = context_id
            
            # Create and send request
            request = SendMessageRequest(
                id=str(uuid4()),
                params=MessageSendParams(**send_message_payload)
            )
            
            logger.info(f"Sending message to parent agent: {message[:100]}...")
            response = await self.client.send_message(request)
            
            # Extract response content
            result = response.model_dump(mode='json', exclude_none=True)
            logger.info("Received response from parent agent")
            
            return self._extract_response_content(result)
            
        except Exception as e:
            logger.error(f"Error communicating with parent agent: {e}")
            raise
    
    def _extract_response_content(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract content from A2A response"""
        try:
            # Handle direct response structure (no 'root' wrapper)
            result = response_data
            if 'root' in response_data and 'result' in response_data['root']:
                result = response_data['root']['result']
            elif 'result' in response_data:
                result = response_data['result']
            
            # Try to extract content from various response formats
            content = None
            
            # Check for artifacts first (most common for completed tasks)
            if 'artifacts' in result and result['artifacts']:
                artifacts = result['artifacts']
                if artifacts and isinstance(artifacts, list) and len(artifacts) > 0:
                    artifact = artifacts[0]
                    if 'parts' in artifact and artifact['parts']:
                        parts = artifact['parts']
                        if parts and isinstance(parts, list) and len(parts) > 0:
                            if 'text' in parts[0]:
                                content = parts[0]['text']
            
            # Fallback to message content
            if not content and 'message' in result and 'parts' in result['message']:
                parts = result['message']['parts']
                if parts and isinstance(parts, list) and len(parts) > 0:
                    if 'text' in parts[0]:
                        content = parts[0]['text']
            
            # If we still don't have content, check the history for the latest agent message
            if not content and 'history' in result:
                history = result['history']
                if isinstance(history, list):
                    # Find the last agent message in history
                    for msg in reversed(history):
                        if msg.get('role') == 'agent' and 'parts' in msg:
                            parts = msg['parts']
                            if parts and isinstance(parts, list) and len(parts) > 0:
                                if 'text' in parts[0]:
                                    # Skip status messages, get actual content
                                    text = parts[0]['text']
                                    if text not in ['Searching for information...', 'Processing the results...']:
                                        content = text
                                        break
            
            # Final fallback - look for any text content in the response
            if not content:
                content = f"Response received but content format unexpected: {result}"
            
            return {
                'content': content,
                'task_id': result.get('id'),
                'context_id': result.get('contextId'),
                'status': result.get('status', {}).get('state', 'completed') if isinstance(result.get('status'), dict) else result.get('status', 'completed')
            }
                
        except Exception as e:
            logger.error(f"Error extracting response content: {e}")
            return {
                'content': f"Error processing response: {str(e)}",
                'status': 'error'
            }
    
    def can_handle_capability(self, capability: str) -> bool:
        """Check if parent agent can handle a specific capability"""
        if not self.parent_agent_card:
            return False
        
        # Check skills for matching capability
        for skill in self.parent_agent_card.skills:
            if capability.lower() in [tag.lower() for tag in skill.tags]:
                return True
            if capability.lower() in skill.id.lower() or capability.lower() in skill.name.lower():
                return True
        
        return False
    
    def get_parent_capabilities(self) -> list[str]:
        """Get list of parent agent capabilities"""
        if not self.parent_agent_card:
            return []
        
        capabilities = []
        for skill in self.parent_agent_card.skills:
            capabilities.extend(skill.tags)
            capabilities.append(skill.id)
        
        return list(set(capabilities))
    
    async def close(self):
        """Close HTTP client connection"""
        if self.httpx_client:
            await self.httpx_client.aclose()