class WebSocketService {
    constructor() {
        this.socket = null
        this.reconnectAttempts = 0
        this.maxReconnectAttempts = 5
        this.reconnectInterval = 3000
        this.listeners = new Map()
    }

    connect(url) {
        try {
            this.socket = new WebSocket(url)

            this.socket.onopen = () => {
                console.log('WebSocket connected')
                this.reconnectAttempts = 0
                this.emit('connected')
            }

            this.socket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data)
                    this.emit('message', data)
                } catch (error) {
                    console.error('Error parsing WebSocket message:', error)
                }
            }

            this.socket.onclose = () => {
                console.log('WebSocket disconnected')
                this.emit('disconnected')
                this.attemptReconnect(url)
            }

            this.socket.onerror = (error) => {
                console.error('WebSocket error:', error)
                this.emit('error', error)
            }

        } catch (error) {
            console.error('WebSocket connection failed:', error)
        }
    }

    attemptReconnect(url) {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++
            console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)

            setTimeout(() => {
                this.connect(url)
            }, this.reconnectInterval * this.reconnectAttempts)
        } else {
            console.error('Max reconnection attempts reached')
            this.emit('reconnect_failed')
        }
    }

    send(message) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify(message))
        } else {
            console.warn('WebSocket is not connected')
        }
    }

    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, new Set())
        }
        this.listeners.get(event).add(callback)
    }

    off(event, callback) {
        if (this.listeners.has(event)) {
            this.listeners.get(event).delete(callback)
        }
    }

    emit(event, data) {
        if (this.listeners.has(event)) {
            this.listeners.get(event).forEach(callback => {
                try {
                    callback(data)
                } catch (error) {
                    console.error(`Error in WebSocket listener for ${event}:`, error)
                }
            })
        }
    }

    disconnect() {
        if (this.socket) {
            this.socket.close()
            this.socket = null
        }
        this.listeners.clear()
    }
}

// Create singleton instance
const webSocketService = new WebSocketService()

export default webSocketService