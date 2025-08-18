import type { AgentCard, TaskResponse, ConversationMessage, RoutingDecision } from '../types/agent'

const CLIENT_BACKEND_URL = 'http://localhost:8000'

export async function getAgentCards(): Promise<{ client: AgentCard, parent: AgentCard }> {
  try {
    const response = await fetch(`${CLIENT_BACKEND_URL}/agent-cards`)
    if (!response.ok) {
      throw new Error(`Failed to fetch agent cards: ${response.statusText}`)
    }
    return await response.json()
  } catch (error) {
    console.error('Error fetching agent cards:', error)
    throw error
  }
}

export async function sendHelloWorldRequest(): Promise<TaskResponse> {
  try {
    const response = await fetch(`${CLIENT_BACKEND_URL}/hello`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    if (!response.ok) {
      throw new Error(`Hello world request failed: ${response.statusText}`)
    }
    return await response.json()
  } catch (error) {
    console.error('Error sending hello world request:', error)
    throw error
  }
}

export async function sendTaskQuery(query: string): Promise<TaskResponse> {
  try {
    const response = await fetch(`${CLIENT_BACKEND_URL}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    })
    if (!response.ok) {
      throw new Error(`Task query failed: ${response.statusText}`)
    }
    return await response.json()
  } catch (error) {
    console.error('Error sending task query:', error)
    throw error
  }
}

export async function getRoutingDecision(query: string): Promise<RoutingDecision> {
  try {
    const response = await fetch(`${CLIENT_BACKEND_URL}/routing-decision`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    })
    if (!response.ok) {
      throw new Error(`Routing decision failed: ${response.statusText}`)
    }
    return await response.json()
  } catch (error) {
    console.error('Error getting routing decision:', error)
    throw error
  }
}

export async function sendChatMessage(
  message: string, 
  conversationId?: string
): Promise<ConversationMessage> {
  try {
    const response = await fetch(`${CLIENT_BACKEND_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        message, 
        conversation_id: conversationId 
      }),
    })
    if (!response.ok) {
      throw new Error(`Chat message failed: ${response.statusText}`)
    }
    return await response.json()
  } catch (error) {
    console.error('Error sending chat message:', error)
    throw error
  }
}