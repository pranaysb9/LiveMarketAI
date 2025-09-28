'use client'

import { useState, useEffect } from 'react'
import UpdateIndicator from './UpdateIndicator'

const LiveFeed = () => {
    const [updates, setUpdates] = useState([])
    const [connectionStatus, setConnectionStatus] = useState('connecting')

    useEffect(() => {
        // In a real implementation, this would connect to WebSocket
        // For now, we'll simulate live updates
        const simulateLiveUpdates = () => {
            const sampleUpdates = [
                {
                    id: 1,
                    type: 'market_data',
                    content: 'AAPL up 1.5% in pre-market trading',
                    symbol: 'AAPL',
                    timestamp: new Date().toLocaleTimeString(),
                    importance: 'medium'
                },
                {
                    id: 2,
                    type: 'news',
                    content: 'Federal Reserve announces interest rate decision',
                    source: 'Reuters',
                    timestamp: new Date().toLocaleTimeString(),
                    importance: 'high'
                },
                {
                    id: 3,
                    type: 'document',
                    content: 'New earnings report added to knowledge base',
                    symbol: 'TSLA',
                    timestamp: new Date().toLocaleTimeString(),
                    importance: 'low'
                }
            ]

            setUpdates(sampleUpdates)
            setConnectionStatus('connected')
        }

        simulateLiveUpdates()

        // Simulate periodic updates
        const interval = setInterval(() => {
            const newUpdate = {
                id: Date.now(),
                type: Math.random() > 0.5 ? 'market_data' : 'news',
                content: `Live update: ${new Date().toLocaleTimeString()}`,
                timestamp: new Date().toLocaleTimeString(),
                importance: ['low', 'medium', 'high'][Math.floor(Math.random() * 3)]
            }

            setUpdates(prev => [newUpdate, ...prev.slice(0, 9)]) // Keep last 10 updates
        }, 10000) // New update every 10 seconds

        return () => clearInterval(interval)
    }, [])

    const getUpdateIcon = (type) => {
        switch (type) {
            case 'market_data':
                return '📈'
            case 'news':
                return '📰'
            case 'document':
                return '📄'
            default:
                return '🔔'
        }
    }

    const getImportanceColor = (importance) => {
        switch (importance) {
            case 'high':
                return 'border-l-red-400 bg-red-50'
            case 'medium':
                return 'border-l-yellow-400 bg-yellow-50'
            case 'low':
                return 'border-l-blue-400 bg-blue-50'
            default:
                return 'border-l-gray-400 bg-gray-50'
        }
    }

    return (
        <div className="h-full flex flex-col">
            {/* Header */}
            <div className="p-4 border-b bg-gray-50">
                <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-gray-900">Live Feed</h3>
                    <UpdateIndicator />
                </div>
                <div className="flex items-center mt-1 space-x-2">
                    <div className={`w-2 h-2 rounded-full ${connectionStatus === 'connected' ? 'bg-green-500' :
                            connectionStatus === 'error' ? 'bg-red-500' : 'bg-yellow-500'
                        }`}></div>
                    <span className="text-xs text-gray-500">
                        {connectionStatus === 'connected' ? 'Live' :
                            connectionStatus === 'error' ? 'Disconnected' : 'Connecting...'}
                    </span>
                </div>
            </div>

            {/* Updates List */}
            <div className="flex-1 overflow-y-auto">
                {updates.length === 0 ? (
                    <div className="p-4 text-center text-gray-500">
                        <div className="w-12 h-12 mx-auto mb-2 bg-gray-100 rounded-full flex items-center justify-center">
                            <span className="text-xl">📊</span>
                        </div>
                        <p className="text-sm">Waiting for live updates...</p>
                    </div>
                ) : (
                    <div className="divide-y">
                        {updates.map((update) => (
                            <div
                                key={update.id}
                                className={`p-4 border-l-4 ${getImportanceColor(update.importance)} hover:bg-white transition-colors`}
                            >
                                <div className="flex items-start space-x-3">
                                    <div className="flex-shrink-0 w-8 h-8 bg-white rounded-full flex items-center justify-center border">
                                        <span className="text-sm">{getUpdateIcon(update.type)}</span>
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
                                            {update.source && (
                                                <span className="text-xs text-gray-500">
                                                    via {update.source}
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Footer */}
            <div className="p-3 border-t bg-gray-50">
                <div className="text-xs text-gray-500 text-center">
                    Real-time financial data and news updates
                </div>
            </div>
        </div>
    )
}

export default LiveFeed