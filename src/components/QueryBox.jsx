'use client'

import { useState } from 'react'

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

export default QueryBox