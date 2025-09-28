import { NextResponse } from 'next/server'

export async function POST(request) {
    try {
        const { query, context, k } = await request.json()

        // Forward the request to the backend API
        const response = await fetch(`http://localhost:8000/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query, context, k }),
        })

        if (!response.ok) {
            throw new Error(`Backend API responded with status: ${response.status}`)
        }

        const data = await response.json()

        return NextResponse.json(data)
    } catch (error) {
        console.error('Chat API route error:', error)
        return NextResponse.json(
            {
                answer: 'Sorry, I encountered an error processing your query. Please try again.',
                sources: [],
                confidence: 0.0,
                error: error.message,
            },
            { status: 500 }
        )
    }
}

export async function GET() {
    return NextResponse.json({ message: 'Chat API is running' })
}