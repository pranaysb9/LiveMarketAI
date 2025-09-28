'use client'

export default function UpdateIndicator({ lastUpdate }) {
  return (
    <div className="flex items-center space-x-2 text-sm text-gray-500">
      <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
      <span>
        {lastUpdate ? `Updated ${lastUpdate}` : 'Live updates'}
      </span>
    </div>
  )
}
