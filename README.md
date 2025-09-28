# LiveMarket AI - Real-Time FinTech RAG System
COuld not add the whole repo in proper structure due to size limitations but to recreate this repo please FOllow this structure
livemarket-ai/
├── backend/
│   ├── pathway_pipeline.py
│   ├── agents/
│   │   ├── market_agent.py
│   │   └── reporter_agent.py
│   ├── rag/
│   │   ├── vector_store.py
│   │   └── rag_engine.py
│   ├── api/
│   │   └── app.py
│   └── data_sources/
│       ├── market_data.py
│       └── news_feeds.py
├── frontend/
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.js
│   │   │   ├── page.js
│   │   │   └── api/
│   │   │       └── chat/route.js
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── MarketChart.jsx
│   │   │   └── NewsFeed.jsx
│   │   └── lib/
│   │       └── websocket.js
│   └── public/
│       └── favicon.ico
├── requirements.txt
├── package.json
├── docker-compose.yml
├── .env.example
├── run.py
└── README.md 


LiveMarketAI is developed and tested on macOS , where the Pathway pipeline runs natively. On Windows, Pathway is not directly supported, so to run the full system, users need to use Docker. Docker provides a consistent environment, allowing Windows users to run the backend, frontend, and Pathway pipeline without compatibility issues, ensuring the demo works exactly as it does on Mac/Linux.
## 🚀 Features

- **Real-Time Market Data**: Live streaming stock prices, crypto, and financial news
- **AI Agents**: Specialized market analysis and reporting agents
- **Dynamic RAG**: Real-time document indexing and retrieval
- **Dual Pipeline**: Pathway streaming engine + FAISS fallback
- **Multi-Embedder**: OpenAI & local sentence-transformers
- **WebSocket Support**: Live updates to React frontend
- **Data Simulator**: Realistic market data generation
- **Production Ready**: Docker, tests, CI/CD

## 🏃 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Linux/macOS/WSL

### One-Command Demo
```bash
# Setup and run complete system
./scripts/demo.sh

