'use client'

export default function NewsFeed() {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Financial News Feed</h2>
      <div className="text-center py-12">
        <div className="w-16 h-16 mx-auto mb-4 bg-purple-100 rounded-full flex items-center justify-center">
          <span className="text-2xl">📰</span>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">Live News Updates</h3>
        <p className="text-gray-500">
          Real-time financial news and market updates will be displayed here.
          Stay informed with the latest market-moving information.
        </p>
      </div>
    </div>
  )
}
