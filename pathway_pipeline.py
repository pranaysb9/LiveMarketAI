"""
Pathway Streaming Pipeline for Real-Time Data Processing
"""

import pathway as pw
import logging
import os
from datetime import datetime
from typing import Dict, Any, List
from pathway.stdlib.ml.index import KNNIndex

logger = logging.getLogger(__name__)

class PathwayPipeline:
    """Real-time streaming pipeline using Pathway"""
    
    def __init__(self, embedder, vector_store):
        self.embedder = embedder
        self.vector_store = vector_store
        self.setup_pipeline()
        
    def setup_pipeline(self):
        """Setup Pathway tables and streaming pipeline"""
        try:
            # Define schema for financial documents
            class FinancialDocument(pw.Schema):
                id: str
                content: str
                timestamp: datetime
                source: str
                symbol: str = None
                embedding: List[float] = None
                metadata: Dict[str, Any] = None
            
            # Create input tables
            self.documents_table = pw.io.json.read(
                "./data/input_documents.json",
                schema=FinancialDocument,
                mode="streaming"
            )
            
            # Add embeddings
            def add_embeddings(doc):
                try:
                    embedding = self.embedder.embed(doc.content)
                    return {
                        **doc,
                        "embedding": embedding,
                        "metadata": {
                            "source": doc.source,
                            "symbol": doc.symbol,
                            "timestamp": doc.timestamp.isoformat()
                        }
                    }
                except Exception as e:
                    logger.error(f"Embedding error: {e}")
                    return doc
            
            self.enriched_documents = self.documents_table.select(
                *pw.this.apply(add_embeddings)
            )
            
            # Build vector index
            self.index = KNNIndex(
                self.enriched_documents.embedding,
                self.enriched_documents,
                n_dimensions=len(self.enriched_documents.embedding[0]),
                n_and=10
            )
            
            # Output to vector store
            pw.io.json.write(
                self.enriched_documents,
                "./data/processed_documents.json"
            )
            
            logger.info("✅ Pathway pipeline setup complete")
            
        except Exception as e:
            logger.error(f"❌ Pathway pipeline setup failed: {e}")
            raise
    
    def add_document(self, content: str, source: str, symbol: str = None) -> str:
        """Add document to streaming pipeline"""
        try:
            doc_id = f"doc_{datetime.now().timestamp()}"
            document = {
                "id": doc_id,
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "source": source,
                "symbol": symbol
            }
            
            # In a real implementation, this would write to Pathway input
            # For demo, we'll directly add to vector store
            embedding = self.embedder.embed(content)
            self.vector_store.add_documents([{
                "content": content,
                "embedding": embedding,
                "metadata": {
                    "source": source,
                    "symbol": symbol,
                    "timestamp": datetime.now().isoformat(),
                    "id": doc_id
                }
            }])
            
            logger.info(f"📄 Document added to pipeline: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"❌ Failed to add document: {e}")
            raise
    
    def query(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Query the streaming index"""
        try:
            # For demo, use vector store directly
            # In full implementation, this would use Pathway's real-time query
            return self.vector_store.search(query, k=k)
        except Exception as e:
            logger.error(f"❌ Query failed: {e}")
            return []

    def run(self):
        """Run the Pathway pipeline"""
        try:
            pw.run()
            logger.info("🔄 Pathway pipeline running")
        except Exception as e:
            logger.error(f"❌ Pipeline run failed: {e}")
            raise