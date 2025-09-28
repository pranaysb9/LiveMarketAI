'use client'

import { useState, useEffect, useRef } from 'react'

const ChatInterface = () => {
  const [conversation, setConversation] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [systemStatus, setSystemStatus] = useState('connected')
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [conversation])

  const handleQuerySubmit = async (query) => {
    if (!query.trim()) return

    // Add user message to conversation
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: query,
      timestamp: new Date().toLocaleTimeString()
    }

    setConversation(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          context: {},
          k: 5
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()

      // Add AI response to conversation
      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: data.answer,
        sources: data.sources,
        confidence: data.confidence,
        agent: data.agent,
        timestamp: new Date().toLocaleTimeString()
      }

      setConversation(prev => [...prev, aiMessage])
      setSystemStatus('connected')

    } catch (error) {
      console.error('Query failed:', error)
      
      const errorMessage = {
        id: Date.now() + 1,
        type: 'error',
        content: 'Sorry, I encountered an error processing your query. Please try again.',
        timestamp: new Date().toLocaleTimeString()
      }

      setConversation(prev => [...prev, errorMessage])
      setSystemStatus('error')
    } finally {
      setIsLoading(false)
    }
  }

  const clearConversation = () => {
    setConversation([])
  }

  return (
    <div className="flex h-[calc(100vh-200px)] bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Chat History */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="p-4 border-b bg-gray-50 rounded-t-lg">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-semibold text-gray-900">AI Financial Assistant</h2>
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${
                systemStatus === 'connected' ? 'bg-green-500' : 
                systemStatus === 'error' ? 'bg-red-500' : 'bg-yellow-500'
              }`}></div>
              <span className="text-sm text-gray-500">
                {systemStatus === 'connected' ? 'Connected' : 
                 systemStatus === 'error' ? 'Error' : 'Connecting...'}
              </span>
              <button
                onClick={clearConversation}
                className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
              >
                Clear Chat
              </button>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {conversation.length === 0 ? (
            <div className="text-center py-12">
              <div className="w-16 h-16 mx-auto mb-4 bg-blue-100 rounded-full flex items-center justify-center">
                <span className="text-2xl">💬</span>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">Start a Conversation</h3>
              <p className="text-gray-500 max-w-md mx-auto">
                Ask about market trends, stock performance, financial news, or investment insights.
                The AI will provide real-time analysis based on current data.
              </p>
              <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-3 max-w-lg mx-auto">
                {[
                  "What's the current market trend?",
                  "How is AAPL performing today?",
                  "Latest cryptocurrency news?",
                  "Investment outlook for tech sector?"
                ].map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => handleQuerySubmit(suggestion)}
                    className="p-3 text-sm text-left bg-gray-50 hover:bg-gray-100 rounded-md border border-gray-200 transition-colors"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            conversation.map((message) => (
              <div
                key={message.id}
                className={`flex ${
                  message.type === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-3xl rounded-lg px-4 py-3 ${
                    message.type === 'user'
                      ? 'bg-blue-600 text-white'
                      : message.type === 'error'
                      ? 'bg-red-100 text-red-800 border border-red-200'
                      : 'bg-gray-100 text-gray-900 border border-gray-200'
                  }`}
                >
                  <div className="whitespace-pre-wrap">{message.content}</div>
                  
                  {message.type === 'ai' && message.sources && message.sources.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-gray-200">
                      <p className="text-sm font-medium text-gray-700 mb-2">Sources:</p>
                      <div className="space-y-1">
                        {message.sources.slice(0, 3).map((source, index) => (
                          <div key={index} className="text-xs text-gray-600">
                            • {source}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  <div className="flex justify-between items-center mt-2">
                    <span className="text-xs opacity-75">
                      {message.timestamp}
                    </span>
                    {message.type === 'ai' && message.confidence && (
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        message.confidence > 0.8
                          ? 'bg-green-100 text-green-800'
                          : message.confidence > 0.6
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {Math.round(message.confidence * 100)}% confidence
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 text-gray-900 rounded-lg px-4 py-3 border border-gray-200 max-w-3xl">
                <div className="flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                  <span className="text-sm text-gray-600">Analyzing your query...</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Query Input */}
        <div className="p-4 border-t">
          <QueryBox onQuerySubmit={handleQuerySubmit} disabled={isLoading} />
        </div>
      </div>

      {/* Live Feed Sidebar */}
      <div className="w-80 border-l border-gray-200">
        <LiveFeed />
      </div>
    </div>
  )
}

const QueryBox = ({ onQuerySubmit, disabled = false }) => {
  const [query, setQuery] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim() && !disabled) {
      onQuerySubmit(query.trim())
      setQuery('')
    }
  }

  const quickQueries = [
    "What's the current market trend?",
    "How is Tesla performing?",
    "Latest financial news",
    "Cryptocurrency market update",
    "Investment recommendations"
  ]

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="flex space-x-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about markets, stocks, or financial news..."
          className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
          disabled={disabled}
        />
        <button
          type="submit"
          disabled={!query.trim() || disabled}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {disabled ? (
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <span>Analyzing...</span>
            </div>
          ) : (
            'Ask'
          )}
        </button>
      </form>

      {/* Quick Query Suggestions */}
      <div className="flex flex-wrap gap-2">
        {quickQueries.map((suggestion, index) => (
          <button
            key={index}
            onClick={() => onQuerySubmit(suggestion)}
            disabled={disabled}
            className="px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 disabled:opacity-50 transition-colors"
          >
            {suggestion}
          </button>
        ))}
      </div>
    </div>
  )
}

const LiveFeed = () => {
  const [updates, setUpdates] = useState([
    {
      id: 1,
      type: 'market_data',
      content: 'AAPL showing strong momentum with 0.68% gain',
      symbol: 'AAPL',
      timestamp: new Date().toLocaleTimeString(),
      importance: 'medium'
    },
    {
      id: 2,
      type: 'news',
      content: 'Tech Stocks Rally on Strong Earnings Reports',
      source: 'Bloomberg',
      timestamp: new Date().toLocaleTimeString(),
      importance: 'high'
    }
  ])

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b bg-gray-50">
        <h3 className="font-semibold text-gray-900">Live Feed</h3>
        <div className="flex items-center mt-1 space-x-2">
          <div className="w-2 h-2 rounded-full bg-green-500"></div>
          <span className="text-xs text-gray-500">Live</span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto">
        <div className="divide-y">
          {updates.map((update) => (
            <div
              key={update.id}
              className={`p-4 border-l-4 ${
                update.importance === 'high' ? 'border-red-400 bg-red-50' :
                update.importance === 'medium' ? 'border-yellow-400 bg-yellow-50' :
                'border-blue-400 bg-blue-50'
              }`}
            >
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-8 h-8 bg-white rounded-full flex items-center justify-center border">
                  <span className="text-sm">
                    {update.type === 'market_data' ? '📈' : '📰'}
                  </span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-900 leading-5">
                    {update.content}
                  </p>
                  <div className="mt-1 flex items-center space-x-2">
                    <span className="text-xs text-gray-500">
                      {update.timestamp}
                    </span>
                    {update.symbol && (
                      <span className="text-xs bg-gray-200 text-gray-700 px-2 py-1 rounded">
                        {update.symbol}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default ChatInterface
