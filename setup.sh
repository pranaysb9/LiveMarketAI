#!/bin/bash

echo "�� Setting up LiveMarket AI..."

# Check if we're in the right directory
if [ ! -f "run.py" ]; then
    echo "❌ Please run this script from the livemarket-ai root directory"
    exit 1
fi

# Fix requirements.txt
echo "📦 Fixing Python dependencies..."
cat > backend/requirements.txt << 'REQUIREMENTS'
pathway==0.8.0
fastapi==0.104.1
uvicorn==0.24.0
openai==1.3.9
sentence-transformers==2.2.2
numpy==1.24.3
pandas==2.1.3
pydantic==2.5.0
python-dotenv==1.0.0
websockets==12.0
aiohttp==3.9.1
requests==2.31.0
pytest==7.4.3
pytest-asyncio==0.21.1
REQUIREMENTS

# Create essential backend files
echo "🐍 Creating backend files..."

# Create a simple API app first
cat > backend/api/app.py << 'APP'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "LiveMarket AI API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/status")
async def status():
    return {
        "pipeline": {"status": "active"},
        "agents": {"market_agent": "active", "reporter_agent": "active"},
        "vector_store": {"document_count": 0}
    }
APP

# Create data simulator
cat > backend/data_sources/data_simulator.py << 'SIMULATOR'
import asyncio
import logging

logger = logging.getLogger(__name__)

async def start_simulator():
    logger.info("📊 Data simulator started")
    while True:
        await asyncio.sleep(10)
SIMULATOR

# Create websocket manager
cat > backend/api/websocket.py << 'WEBSOCKET'
from fastapi import WebSocket
from typing import List

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def start(self):
        pass

websocket_manager = WebSocketManager()
WEBSOCKET

# Fix frontend structure
echo "📱 Fixing frontend structure..."

# Create tailwind config
cat > frontend/tailwind.config.js << 'TAILWIND'
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
TAILWIND

# Create globals.css
cat > frontend/src/styles/globals.css << 'CSS'
@tailwind base;
@tailwind components;
@tailwind utilities;
CSS

# Create a simple Dashboard component
cat > frontend/src/components/Dashboard.jsx << 'DASHBOARD'
export default function Dashboard() {
  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-semibold">System Status</h3>
          <p className="text-green-600">All Systems Operational</p>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-semibold">Documents</h3>
          <p>0 documents indexed</p>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-semibold">Live Updates</h3>
          <p>Ready for real-time data</p>
        </div>
      </div>
    </div>
  )
}
DASHBOARD

# Create environment file
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
fi

echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Edit .env file with your OpenAI API key"
echo "   2. Run: cd backend && source venv/bin/activate && pip install -r requirements.txt"
echo "   3. Run: python run.py"
echo "   4. In another terminal: cd frontend && npm run dev"
echo "   5. Open http://localhost:3000"
