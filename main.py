"""
Backend Main Module
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/status")
def status():
    return {"status": "ok"}
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class LiveMarketAI:
    def __init__(self):
        self.embedder = None
        self.vector_store = None
        self.pipeline = None
        self.market_agent = None
        self.reporter_agent = None
        self.setup_components()
    
    def setup_components(self):
        try:
            from backend.rag.embeddings import Embedder
            from backend.rag.vector_store import VectorStore
            from backend.agents.market_agent import MarketAgent
            from backend.agents.reporter_agent import ReporterAgent
            
            self.embedder = Embedder()
            self.vector_store = VectorStore(self.embedder)
            
            use_pathway = os.getenv('USE_PATHWAY', 'false').lower() == 'true'
            if use_pathway:
                try:
                    from backend.pathway_pipeline import PathwayPipeline
                    self.pipeline = PathwayPipeline(self.embedder, self.vector_store)
                    logger.info("🚀 Using Pathway streaming pipeline")
                except ImportError:
                    logger.warning("❌ Pathway not available, falling back to in-memory")
                    from backend.in_memory_pipeline import InMemoryPipeline
                    self.pipeline = InMemoryPipeline(self.embedder, self.vector_store)
            else:
                from backend.in_memory_pipeline import InMemoryPipeline
                self.pipeline = InMemoryPipeline(self.embedder, self.vector_store)
                logger.info("💾 Using in-memory pipeline")
            
            if os.getenv('MARKET_AGENT_ENABLED', 'true').lower() == 'true':
                self.market_agent = MarketAgent(self.pipeline)
                logger.info("🤖 Market agent initialized")
            
            if os.getenv('REPORTER_AGENT_ENABLED', 'true').lower() == 'true':
                self.reporter_agent = ReporterAgent(self.pipeline)
                logger.info("📊 Reporter agent initialized")
            
            logger.info("✅ All components initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Component initialization failed: {e}")
            raise
    
    def process_query(self, query: str, context: dict = None) -> dict:
        try:
            retrieved_docs = self.pipeline.query(query, k=5)
            
            if self._is_market_query(query) and self.market_agent:
                response = self.market_agent.analyze(query, retrieved_docs, context)
            elif self.reporter_agent:
                response = self.reporter_agent.generate_report(query, retrieved_docs, context)
            else:
                response = {
                    "answer": "I'm currently unable to process this query.",
                    "sources": [],
                    "confidence": 0.0
                }
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Query processing failed: {e}")
            return {
                "answer": "Sorry, I encountered an error processing your query.",
                "sources": [],
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _is_market_query(self, query: str) -> bool:
        market_keywords = ['price', 'stock', 'market', 'trade', 'investment', 'crypto']
        return any(keyword in query.lower() for keyword in market_keywords)
    
    def add_document(self, content: str, source: str, symbol: str = None) -> str:
        return self.pipeline.add_document(content, source, symbol)
    
    def get_system_status(self) -> dict:
        return {
            "pipeline": self.pipeline.get_stats() if hasattr(self.pipeline, 'get_stats') else {"status": "active"},
            "agents": {
                "market_agent": "active" if self.market_agent else "inactive",
                "reporter_agent": "active" if self.reporter_agent else "inactive"
            },
            "vector_store": {
                "document_count": len(self.vector_store.documents) if hasattr(self.vector_store, 'documents') else 0
            }
        }

livemarket_ai = LiveMarketAI()
