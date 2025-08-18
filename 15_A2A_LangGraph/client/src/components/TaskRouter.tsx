import { useState } from 'react'
import type { AgentCard, TaskResponse, RoutingDecision } from '../types/agent'
import { sendHelloWorldRequest, sendTaskQuery, getRoutingDecision } from '../services/api'

interface TaskRouterProps {
  clientAgent: AgentCard | null
  parentAgent: AgentCard | null
}

export default function TaskRouter({ }: TaskRouterProps) {
  const [response, setResponse] = useState<TaskResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [routingInfo, setRoutingInfo] = useState<RoutingDecision | null>(null)
  const [customQuery, setCustomQuery] = useState('')

  const handleHelloWorld = async () => {
    setLoading(true)
    setRoutingInfo(null)
    try {
      const result = await sendHelloWorldRequest()
      setResponse(result)
    } catch (error) {
      setResponse({
        content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        agent_source: 'client'
      })
    } finally {
      setLoading(false)
    }
  }

  const handleCustomQuery = async (query: string) => {
    if (!query.trim()) return
    
    setLoading(true)
    setResponse(null)
    setRoutingInfo(null)
    
    try {
      // First get routing decision
      const routing = await getRoutingDecision(query)
      setRoutingInfo(routing)
      
      // Then execute the query
      const result = await sendTaskQuery(query)
      setResponse(result)
    } catch (error) {
      setResponse({
        content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        agent_source: 'client'
      })
    } finally {
      setLoading(false)
    }
  }

  const predefinedQueries = [
    {
      label: "Latest AI Research",
      query: "Find recent papers on transformer architectures",
      expectedAgent: "parent",
      reason: "Requires ArXiv academic search capability"
    },
    {
      label: "Simple Math",
      query: "What is 15 * 23?",
      expectedAgent: "client", 
      reason: "Basic calculation can be handled locally"
    },
    {
      label: "Web Search Task",
      query: "What are the latest developments in artificial intelligence?",
      expectedAgent: "parent",
      reason: "Requires Tavily web search capability"
    },
    {
      label: "Hello Greeting",
      query: "Say hello and tell me the current time",
      expectedAgent: "client",
      reason: "Simple greeting with timestamp generation"
    }
  ]

  return (
    <section>
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">
          🎯 Intelligent Task Routing
        </h2>
        <p className="text-gray-600 text-lg max-w-3xl mx-auto">
          This demonstrates how the A2A protocol enables intelligent routing based on agent 
          capabilities. The client agent decides whether to handle tasks locally or delegate 
          to the parent agent via A2A communication.
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Control Panel */}
        <div className="space-y-6">
          <div className="bg-white/70 backdrop-blur-sm rounded-xl shadow-xl p-8 border border-gray-200/50">
            <h3 className="text-xl font-bold mb-6 text-gray-800 flex items-center">
              🎮 Task Controls
            </h3>
            
            {/* Hello World Button */}
            <div className="mb-4">
              <button
                onClick={handleHelloWorld}
                disabled={loading}
                className="w-full px-6 py-4 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl hover:from-blue-600 hover:to-blue-700 disabled:opacity-50 font-semibold text-lg transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                {loading ? '⏳ Processing...' : '🏠 Local Hello World'}
              </button>
              <p className="text-xs text-gray-500 mt-1">
                Always handled by client agent locally
              </p>
            </div>

            {/* Predefined Queries */}
            <div className="space-y-2">
              <h4 className="font-medium text-gray-700">Predefined Queries:</h4>
              {predefinedQueries.map((item, index) => (
                <div key={index} className="border rounded p-3">
                  <button
                    onClick={() => handleCustomQuery(item.query)}
                    disabled={loading}
                    className="w-full text-left px-3 py-2 bg-gray-50 hover:bg-gray-100 rounded text-sm"
                  >
                    {item.label}
                  </button>
                  <p className="text-xs text-gray-500 mt-1">
                    Expected: {item.expectedAgent} agent - {item.reason}
                  </p>
                </div>
              ))}
            </div>

            {/* Custom Query */}
            <div className="mt-4">
              <h4 className="font-medium text-gray-700 mb-2">Custom Query:</h4>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={customQuery}
                  onChange={(e) => setCustomQuery(e.target.value)}
                  placeholder="Enter your question..."
                  className="flex-1 px-3 py-2 border border-gray-300 rounded text-sm"
                  onKeyPress={(e) => e.key === 'Enter' && handleCustomQuery(customQuery)}
                />
                <button
                  onClick={() => handleCustomQuery(customQuery)}
                  disabled={loading || !customQuery.trim()}
                  className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:opacity-50 text-sm"
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Response Panel */}
        <div className="bg-white/70 backdrop-blur-sm rounded-xl shadow-xl p-8 border border-gray-200/50">
          <h3 className="text-xl font-bold mb-6 text-gray-800 flex items-center">
            💬 Response & Routing
          </h3>
          
          {loading && (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
              <p className="mt-2 text-gray-600">Processing request...</p>
            </div>
          )}

          {routingInfo && (
            <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded">
              <h4 className="font-medium text-yellow-800">🎯 Routing Decision:</h4>
              <p className="text-sm text-yellow-700">
                <strong>Agent:</strong> {routingInfo.route_to} 
                <span className="ml-2">
                  <strong>Confidence:</strong> {(routingInfo.confidence * 100).toFixed(1)}%
                </span>
              </p>
              <p className="text-sm text-yellow-700 mt-1">
                <strong>Reason:</strong> {routingInfo.reason}
              </p>
            </div>
          )}

          {response && (
            <div className="space-y-3">
              <div className={`p-3 rounded border-l-4 ${
                response.agent_source === 'client' 
                  ? 'bg-blue-50 border-blue-400' 
                  : 'bg-green-50 border-green-400'
              }`}>
                <div className="flex items-center justify-between mb-2">
                  <span className={`text-sm font-medium ${
                    response.agent_source === 'client' ? 'text-blue-800' : 'text-green-800'
                  }`}>
                    {response.agent_source === 'client' ? '🏠 Client Agent' : '🌐 Parent Agent (A2A)'}
                  </span>
                  {response.execution_time && (
                    <span className="text-xs text-gray-500">
                      {response.execution_time}ms
                    </span>
                  )}
                </div>
                <p className="text-sm text-gray-700 whitespace-pre-wrap">
                  {response.content}
                </p>
                {response.routing_decision && (
                  <p className="text-xs text-gray-500 mt-2 italic">
                    Routing: {response.routing_decision}
                  </p>
                )}
              </div>
            </div>
          )}

          {!loading && !response && (
            <div className="text-center py-8 text-gray-500">
              Click a button above to see A2A routing in action
            </div>
          )}
        </div>
      </div>

      <div className="mt-8 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200/50 rounded-xl p-6 shadow-lg">
        <h4 className="font-bold text-green-800 mb-4 text-lg">🚀 A2A Protocol Benefits</h4>
        <div className="grid md:grid-cols-2 gap-3">
          <div className="flex items-start space-x-2">
            <span className="text-green-600 font-bold">•</span>
            <div>
              <strong className="text-green-800">Automatic Capability Discovery:</strong>
              <span className="text-green-700 text-sm block">Client agent knows what parent can do</span>
            </div>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-green-600 font-bold">•</span>
            <div>
              <strong className="text-green-800">Intelligent Routing:</strong>
              <span className="text-green-700 text-sm block">Tasks go to the most appropriate agent</span>
            </div>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-green-600 font-bold">•</span>
            <div>
              <strong className="text-green-800">Standardized Communication:</strong>
              <span className="text-green-700 text-sm block">Same protocol works across different agents</span>
            </div>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-green-600 font-bold">•</span>
            <div>
              <strong className="text-green-800">Scalable Architecture:</strong>
              <span className="text-green-700 text-sm block">Easy to add more specialized agents</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}