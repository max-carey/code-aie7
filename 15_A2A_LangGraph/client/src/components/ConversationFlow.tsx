import { useState } from 'react'
import type { ConversationMessage } from '../types/agent'
import { sendChatMessage } from '../services/api'

export default function ConversationFlow() {
  const [messages, setMessages] = useState<ConversationMessage[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [conversationId] = useState(() => `conv_${Date.now()}`)

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return

    const userMessage: ConversationMessage = {
      id: `msg_${Date.now()}`,
      role: 'user',
      content: inputMessage,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setLoading(true)

    try {
      const response = await sendChatMessage(inputMessage, conversationId)
      setMessages(prev => [...prev, response])
    } catch (error) {
      const errorMessage: ConversationMessage = {
        id: `error_${Date.now()}`,
        role: 'assistant',
        content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        timestamp: new Date(),
        agent_source: 'client'
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const clearConversation = () => {
    setMessages([])
  }

  const suggestedQueries = [
    "Hello! Can you help me with research?",
    "Find papers on machine learning",
    "What's 25 * 16?",
    "Search for latest AI news",
    "Can you summarize what we've discussed?"
  ]

  return (
    <section>
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">
          💬 Multi-Turn A2A Conversation
        </h2>
        <p className="text-gray-600 text-lg max-w-3xl mx-auto">
          This demonstrates multi-turn conversations that span both agents. The client agent 
          maintains conversation context while intelligently routing individual messages 
          through the A2A protocol when needed.
        </p>
      </div>

      <div className="bg-white/70 backdrop-blur-sm rounded-xl shadow-xl border border-gray-200/50">
        {/* Conversation Header */}
        <div className="p-4 border-b border-gray-200 flex justify-between items-center">
          <div>
            <h3 className="font-semibold text-gray-800">Conversation</h3>
            <p className="text-sm text-gray-500">ID: {conversationId}</p>
          </div>
          <button
            onClick={clearConversation}
            className="px-3 py-1 text-sm bg-gray-100 text-gray-600 rounded hover:bg-gray-200"
          >
            Clear
          </button>
        </div>

        {/* Messages Area */}
        <div className="h-96 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-500 mb-4">Start a conversation to see A2A routing in action!</p>
              <div className="space-y-2">
                <p className="text-sm text-gray-400">Suggested queries:</p>
                {suggestedQueries.map((query, index) => (
                  <button
                    key={index}
                    onClick={() => setInputMessage(query)}
                    className="block mx-auto px-3 py-1 text-sm bg-gray-50 text-gray-600 rounded hover:bg-gray-100"
                  >
                    "{query}"
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                    message.role === 'user'
                      ? 'bg-blue-500 text-white'
                      : message.agent_source === 'client'
                      ? 'bg-blue-100 text-gray-800 border border-blue-200'
                      : 'bg-green-100 text-gray-800 border border-green-200'
                  }`}
                >
                  {message.role === 'assistant' && (
                    <div className="flex items-center justify-between mb-1">
                      <span className={`text-xs font-medium ${
                        message.agent_source === 'client' ? 'text-blue-600' : 'text-green-600'
                      }`}>
                        {message.agent_source === 'client' ? '🏠 Client' : '🌐 Parent (A2A)'}
                      </span>
                      <span className="text-xs text-gray-500">
                        {message.timestamp.toLocaleTimeString()}
                      </span>
                    </div>
                  )}
                  
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  
                  {message.routing_info && (
                    <div className="mt-2 p-2 bg-white bg-opacity-50 rounded text-xs">
                      <p><strong>Routed:</strong> {message.routing_info.decision}</p>
                      <p><strong>Reason:</strong> {message.routing_info.reason}</p>
                    </div>
                  )}
                  
                  {message.role === 'user' && (
                    <div className="text-xs text-blue-200 mt-1">
                      {message.timestamp.toLocaleTimeString()}
                    </div>
                  )}
                </div>
              </div>
            ))
          )}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-lg px-4 py-2">
                <div className="flex items-center space-x-2">
                  <div className="animate-pulse flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                  </div>
                  <span className="text-sm text-gray-600">Processing...</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-gray-200">
          <div className="flex space-x-2">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              onKeyPress={(e) => e.key === 'Enter' && !loading && handleSendMessage()}
              disabled={loading}
            />
            <button
              onClick={handleSendMessage}
              disabled={loading || !inputMessage.trim()}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
            >
              Send
            </button>
          </div>
        </div>
      </div>

      <div className="mt-6 bg-purple-50 border border-purple-200 rounded-lg p-4">
        <h4 className="font-semibold text-purple-800 mb-2">💬 Multi-Turn A2A Benefits:</h4>
        <ul className="text-purple-700 text-sm space-y-1">
          <li>• <strong>Context Preservation:</strong> Conversation state maintained across agents</li>
          <li>• <strong>Intelligent Per-Message Routing:</strong> Each message routed based on content</li>
          <li>• <strong>Seamless User Experience:</strong> User doesn't need to know which agent responds</li>
          <li>• <strong>Protocol Transparency:</strong> A2A communication is invisible to end user</li>
        </ul>
      </div>
    </section>
  )
}