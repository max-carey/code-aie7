import { useState, useEffect } from 'react'
import AgentComparison from './components/AgentComparison'
import TaskRouter from './components/TaskRouter'
import ConversationFlow from './components/ConversationFlow'
import type { AgentCard } from './types/agent'
import { getAgentCards } from './services/api'

function App() {
  const [clientAgent, setClientAgent] = useState<AgentCard | null>(null)
  const [parentAgent, setParentAgent] = useState<AgentCard | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadAgentCards = async () => {
      try {
        setLoading(true)
        const agents = await getAgentCards()
        setClientAgent(agents.client)
        setParentAgent(agents.parent)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load agent cards')
      } finally {
        setLoading(false)
      }
    }

    loadAgentCards()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading A2A Agent Cards...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-xl mb-4">⚠️ Error</div>
          <p className="text-gray-600">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <header className="bg-white/80 backdrop-blur-sm shadow-lg border-b border-gray-200/50">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
              A2A Protocol Showcase
            </h1>
            <p className="mt-3 text-lg text-gray-600 max-w-2xl mx-auto">
              Demonstrating intelligent Agent-to-Agent communication with specialized capabilities and routing
            </p>
            <div className="mt-4 flex justify-center space-x-4 text-sm text-gray-500">
              <span className="flex items-center"><span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>Client Agent (Local)</span>
              <span className="flex items-center"><span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>Parent Agent (A2A)</span>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-12 space-y-12">
        <AgentComparison 
          clientAgent={clientAgent} 
          parentAgent={parentAgent} 
        />
        
        <TaskRouter 
          clientAgent={clientAgent} 
          parentAgent={parentAgent} 
        />
        
        <ConversationFlow />
      </main>
      
      <footer className="bg-gray-50/50 border-t border-gray-200/50 py-8 text-center text-gray-500 text-sm">
        <p>Built with React, FastAPI, LangGraph, and the A2A Protocol</p>
      </footer>
    </div>
  )
}

export default App
