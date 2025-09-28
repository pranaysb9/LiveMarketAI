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
