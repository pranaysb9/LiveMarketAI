# LiveMarket AI - System Architecture

## Overview

LiveMarket AI is a real-time FinTech RAG (Retrieval-Augmented Generation) system that processes live financial data streams to provide intelligent market analysis and insights.

## System Components

### 1. Data Ingestion Layer
- **Market Data Source**: Real-time stock prices, crypto data, market indices
- **News Feed Source**: Financial news articles and market analysis
- **Data Simulator**: Generates realistic financial data for demo purposes

### 2. Streaming Engine
- **Pathway Pipeline**: Real-time data processing with automatic indexing
- **In-Memory Fallback**: FAISS-based pipeline when Pathway is unavailable
- **Vector Store**: FAISS for efficient similarity search

### 3. AI Agents Layer
- **Market Agent**: Specialized in market analysis and trading signals
- **Reporter Agent**: Generates comprehensive financial reports

### 4. RAG Engine
- **Embedding Service**: OpenAI and local sentence-transformers
- **Retrieval System**: Semantic search with similarity scoring
- **Response Generation**: Context-aware AI responses

### 5. API Layer
- **REST API**: FastAPI endpoints for queries and document management
- **WebSocket Server**: Real-time updates and live feeds
- **CORS & Security**: Proper CORS configuration and error handling

### 6. Frontend Layer
- **Next.js React App**: Modern React with App Router
- **Real-time UI**: Live updates via WebSocket
- **Charting**: Recharts for market data visualization
- **Responsive Design**: Tailwind CSS for modern UI

## Data Flow

1. **Real-time Ingestion** → Market data and news feeds are continuously ingested
2. **Stream Processing** → Pathway processes and indexes data in real-time
3. **Vector Storage** → Documents are embedded and stored in FAISS
4. **Query Processing** → User queries trigger semantic search and AI generation
5. **Real-time Updates** → WebSocket broadcasts updates to connected clients

## Technology Stack

### Backend
- **Python 3.11+**: Core programming language
- **Pathway**: Real-time data processing engine
- **FastAPI**: Modern async web framework
- **FAISS**: Vector similarity search
- **OpenAI**: Embeddings and chat completion
- **Sentence-Transformers**: Local embedding fallback

### Frontend
- **Next.js 14**: React framework with App Router
- **Tailwind CSS**: Utility-first CSS framework
- **Recharts**: React charting library
- **WebSocket**: Real-time client communication

### Deployment
- **Docker**: Containerization
- **Docker Compose**: Multi-service orchestration

## Real-time Features

- Live market data streaming
- Dynamic document indexing
- Instant RAG response updates
- WebSocket-based live feeds
- Real-time market charts

## Scalability Considerations

- Pathway's distributed computing capabilities
- FAISS index sharding for large datasets
- WebSocket connection pooling
- Async/await patterns throughout
- Efficient batch processing

## Security Features

- Environment variable configuration
- CORS middleware
- Input validation with Pydantic
- Error handling and logging
- API rate limiting (can be added)