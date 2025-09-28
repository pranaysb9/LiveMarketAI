import '../styles/globals.css'

export const metadata = {
    title: 'LiveMarket AI - Real-Time Financial Intelligence',
    description: 'Real-time FinTech RAG system with live market data and AI analysis',
}

export default function RootLayout({ children }) {
    return (
        <html lang="en">
            <body className="bg-gray-50 text-gray-900">
                {children}
            </body>
        </html>
    )
}
