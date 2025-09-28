# LiveMarket AI - Real-Time FinTech RAG System
DEMO VIDEO https://drive.google.com/file/d/1B17y3lqEn5I2sa0BxIAidR3KYVtv99xj/view?usp=drive_link
COuld not add the whole repo in proper structure due to size limitations but to recreate this repo please FOllow this structure


<img width="82" height="311" alt="image" src="https://github.com/user-attachments/assets/fe006cf0-3cfe-43b4-b291-1b515ca8f117" />


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

