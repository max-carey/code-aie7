import type { AgentCard } from '../types/agent'

interface AgentComparisonProps {
  clientAgent: AgentCard | null
  parentAgent: AgentCard | null
}

export default function AgentComparison({ clientAgent, parentAgent }: AgentComparisonProps) {
  const AgentCardComponent = ({ agent, title, color, icon }: { 
    agent: AgentCard | null, 
    title: string, 
    color: string,
    icon: string
  }) => (
    <div className={`bg-white/70 backdrop-blur-sm rounded-xl shadow-xl p-8 border border-gray-200/50 hover:shadow-2xl transition-all duration-300 ${color}`}>
      <div className="flex items-center mb-4">
        <span className="text-3xl mr-3">{icon}</span>
        <h3 className="text-2xl font-bold text-gray-800">{title}</h3>
      </div>
      {agent ? (
        <div className="space-y-4">
          <div>
            <h4 className="font-semibold text-gray-800">{agent.name}</h4>
            <p className="text-gray-600 text-sm">{agent.description}</p>
            <p className="text-xs text-gray-500 mt-1">Version: {agent.version}</p>
          </div>
          
          <div>
            <h5 className="font-semibold text-gray-700 mb-3">Capabilities</h5>
            <div className="flex flex-wrap gap-2">
              {agent.capabilities.streaming && (
                <span className="px-3 py-2 bg-blue-100 text-blue-800 text-sm rounded-full font-medium">
                  ⚡ Streaming
                </span>
              )}
              {agent.capabilities.push_notifications && (
                <span className="px-3 py-2 bg-green-100 text-green-800 text-sm rounded-full font-medium">
                  🔔 Push Notifications
                </span>
              )}
            </div>
          </div>

          <div>
            <h5 className="font-semibold text-gray-700 mb-3">Skills</h5>
            <div className="space-y-4">
              {agent.skills.map((skill, index) => (
                <div key={index} className="bg-gray-50/50 rounded-lg p-4 border-l-4 border-indigo-400">
                  <h6 className="font-semibold text-gray-800 text-sm mb-1">{skill.name}</h6>
                  <p className="text-xs text-gray-600 mb-2">{skill.description}</p>
                  <div className="flex flex-wrap gap-1 mb-2">
                    {skill.tags.map((tag, tagIndex) => (
                      <span 
                        key={tagIndex}
                        className="px-2 py-1 bg-indigo-100 text-indigo-700 text-xs rounded-md font-medium"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                  {skill.examples.length > 0 && (
                    <div className="mt-2">
                      <p className="text-xs text-gray-500 italic bg-white/50 rounded px-2 py-1">
                        💡 Example: "{skill.examples[0]}"
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : (
        <div className="text-gray-500">Loading agent information...</div>
      )}
    </div>
  )

  return (
    <section>
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">
          🤖 Agent Capabilities Comparison
        </h2>
        <p className="text-gray-600 text-lg max-w-3xl mx-auto">
          This demonstrates the A2A protocol's agent discovery feature. Each agent advertises 
          its capabilities, enabling intelligent task routing based on specialization.
        </p>
      </div>
      
      <div className="grid lg:grid-cols-2 gap-8">
        <AgentCardComponent 
          agent={clientAgent} 
          title="Client Agent (Local)" 
          color="border-l-4 border-blue-500" 
          icon="🏠"
        />
        <AgentCardComponent 
          agent={parentAgent} 
          title="Parent Agent (A2A)" 
          color="border-l-4 border-green-500" 
          icon="🌐"
        />
      </div>

      <div className="mt-8 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200/50 rounded-xl p-6 shadow-lg">
        <h4 className="font-bold text-blue-800 mb-3 text-lg">🔍 A2A Protocol Benefit</h4>
        <p className="text-blue-700">
          Notice how each agent declares different skills and capabilities. The A2A protocol 
          enables automatic discovery of these capabilities, allowing the client agent to 
          intelligently route tasks to the most appropriate agent without hardcoding integrations.
        </p>
      </div>
    </section>
  )
}