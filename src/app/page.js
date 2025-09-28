'use client'

import { useState, useEffect } from 'react'
import Dashboard from '../components/Dashboard'
import ChatInterface from '../components/ChatInterface'
import MarketChart from '../components/MarketChart'
import NewsFeed from '../components/NewsFeed'
import UpdateIndicator from '../components/UpdateIndicator'

export default function Home() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [systemStatus, setSystemStatus] = useState({ status: 'loading' })
  const [lastUpdate, setLastUpdate] = useState(null)

  useEffect(() => {
    fetchSystemStatus()
    const interval = setInterval(fetchSystemStatus, 30000)
    return () => clearInterval(interval)
  }, [])

  const fetchSystemStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/status')
      const status = await response.json()
      setSystemStatus(status)
      setLastUpdate(new Date().toLocaleTimeString())
    } catch (error) {
      console.error('Failed to fetch system status:', error)
      setSystemStatus({ status: 'error', error: error.message })
    }
  }

  const renderTabContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />
      case 'chat':
        return <ChatInterface />
      case 'markets':
        return <MarketChart />
      case 'news':
        return <NewsFeed />
      default:
        return <Dashboard />
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-2xl font-bold text-gray-900">
                  LiveMarket AI
                </h1>
                <p className="text-sm text-gray-500">
                  Real-time Financial Intelligence
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <UpdateIndicator lastUpdate={lastUpdate} />
              <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                systemStatus.status === 'loading' ? 'bg-yellow-100 text-yellow-800' :
                systemStatus.status === 'error' ? 'bg-red-100 text-red-800' :
                'bg-green-100 text-green-800'
              }`}>
                {systemStatus.status === 'loading' ? 'Connecting...' :
                 systemStatus.status === 'error' ? 'Connection Error' : 'System Online'}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {[
              { id: 'dashboard', label: 'Dashboard', icon: '📊' },
              { id: 'chat', label: 'AI Chat', icon: '🤖' },
              { id: 'markets', label: 'Market Data', icon: '📈' },
              { id: 'news', label: 'News Feed', icon: '📰' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {renderTabContent()}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <p className="text-sm text-gray-500">
              © 2024 LiveMarket AI. Real-time FinTech RAG System.
            </p>
            <div className="flex space-x-4">
              <span className="text-xs text-gray-400">
                Pathway Streaming Engine • OpenAI Integration • Real-time Updates
              </span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
