import axios from 'axios'

const API_BASE_URL = process.env.BACKEND_URL || 'http://localhost:8000'

class ApiService {
    constructor() {
        this.client = axios.create({
            baseURL: API_BASE_URL,
            timeout: 30000,
            headers: {
                'Content-Type': 'application/json',
            },
        })

        // Add response interceptor for error handling
        this.client.interceptors.response.use(
            (response) => response,
            (error) => {
                console.error('API request failed:', error)
                throw error
            }
        )
    }

    async healthCheck() {
        const response = await this.client.get('/health')
        return response.data
    }

    async getSystemStatus() {
        const response = await this.client.get('/status')
        return response.data
    }

    async processQuery(query, context = {}, k = 5) {
        const response = await this.client.post('/query', {
            query,
            context,
            k,
        })
        return response.data
    }

    async addDocument(content, source, symbol = null) {
        const response = await this.client.post('/documents', {
            content,
            source,
            symbol,
        })
        return response.data
    }

    async getDocumentCount() {
        const response = await this.client.get('/documents/count')
        return response.data
    }

    // Batch operations
    async addDocuments(documents) {
        const promises = documents.map(doc => this.addDocument(doc.content, doc.source, doc.symbol))
        return Promise.all(promises)
    }

    // Utility methods
    isOnline() {
        return navigator.onLine
    }

    getApiUrl() {
        return API_BASE_URL
    }
}

// Create singleton instance
const apiService = new ApiService()

export default apiService