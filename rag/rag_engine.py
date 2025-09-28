"""
RAG Engine - Core Retrieval Augmented Generation Logic
"""

import logging
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class RAGEngine:
    """Core RAG engine coordinating retrieval and generation"""
    
    def __init__(self, pipeline, embedder, vector_store):
        self.pipeline = pipeline
        self.embedder = embedder
        self.vector_store = vector_store
        logger.info("✅ RAG engine initialized")
    
    def process_query(self, query: str, context: Dict = None, k: int = 5) -> Dict[str, Any]:
        """Process query through full RAG pipeline"""
        try:
            # Step 1: Retrieve relevant documents
            retrieved_docs = self.retrieve(query, k=k)
            
            # Step 2: Generate response using pipeline
            response = self.pipeline.process_query(query, retrieved_docs, context)
            
            # Step 3: Enhance with RAG-specific metadata
            enhanced_response = self._enhance_response(response, retrieved_docs)
            
            logger.info(f"🤖 RAG processed query: '{query}' -> {len(retrieved_docs)} docs")
            return enhanced_response
            
        except Exception as e:
            logger.error(f"❌ RAG processing failed: {e}")
            return {
                "answer": "I encountered an error processing your query. Please try again.",
                "sources": [],
                "confidence": 0.0,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for query"""
        try:
            return self.vector_store.search(query, k=k)
        except Exception as e:
            logger.error(f"❌ Retrieval failed: {e}")
            return []
    
    def _enhance_response(self, response: Dict[str, Any], retrieved_docs: List[Dict]) -> Dict[str, Any]:
        """Enhance response with RAG-specific metadata"""
        # Calculate retrieval quality metrics
        avg_similarity = self._calculate_avg_similarity(retrieved_docs)
        source_diversity = self._calculate_source_diversity(retrieved_docs)
        
        enhanced = {
            **response,
            "rag_metadata": {
                "retrieved_documents_count": len(retrieved_docs),
                "average_similarity_score": avg_similarity,
                "source_diversity": source_diversity,
                "retrieval_timestamp": datetime.now().isoformat()
            }
        }
        
        return enhanced
    
    def _calculate_avg_similarity(self, docs: List[Dict]) -> float:
        """Calculate average similarity score of retrieved documents"""
        if not docs:
            return 0.0
        
        scores = [doc.get('similarity_score', 0.0) for doc in docs]
        return sum(scores) / len(scores)
    
    def _calculate_source_diversity(self, docs: List[Dict]) -> int:
        """Calculate number of unique sources in retrieved documents"""
        if not docs:
            return 0
        
        sources = set()
        for doc in docs:
            metadata = doc.get('metadata', {})
            source = metadata.get('source', 'unknown')
            sources.add(source)
        
        return len(sources)
    
    def add_document(self, content: str, source: str, symbol: str = None) -> str:
        """Add document to RAG system"""
        return self.pipeline.add_document(content, source, symbol)
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get RAG system health status"""
        return {
            "vector_store": self.vector_store.get_stats(),
            "pipeline": self.pipeline.get_stats() if hasattr(self.pipeline, 'get_stats') else {"status": "active"},
            "embedder": {
                "type": self.embedder.embedder_type,
                "dimension": self.embedder.dimension
            },
            "timestamp": datetime.now().isoformat()
        }