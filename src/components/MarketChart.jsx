'use client'

export default function MarketChart() {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Market Data & Charts</h2>
      <div className="text-center py-12">
        <div className="w-16 h-16 mx-auto mb-4 bg-green-100 rounded-full flex items-center justify-center">
          <span className="text-2xl">📈</span>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">Live Market Charts</h3>
        <p className="text-gray-500">
          Real-time market data visualization will be displayed here.
          This includes stock charts, crypto prices, and market indices.
        </p>
      </div>
    </div>
  )
}
