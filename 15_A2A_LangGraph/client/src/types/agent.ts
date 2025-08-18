export interface AgentSkill {
  id: string
  name: string
  description: string
  tags: string[]
  examples: string[]
}

export interface AgentCapabilities {
  streaming: boolean
  push_notifications: boolean
}

export interface AgentCard {
  name: string
  description: string
  url: string
  version: string
  default_input_modes: string[]
  default_output_modes: string[]
  capabilities: AgentCapabilities
  skills: AgentSkill[]
}

export interface TaskResponse {
  content: string
  agent_source: 'client' | 'parent'
  routing_decision?: string
  execution_time?: number
}

export interface ConversationMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  agent_source?: 'client' | 'parent'
  routing_info?: {
    decision: string
    reason: string
  }
}

export interface RoutingDecision {
  route_to: 'client' | 'parent'
  reason: string
  confidence: number
}