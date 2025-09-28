"""
In-Memory Pipeline Fallback (FAISS-based)
"""

import logging
import numpy as np
from datetime import datetime
from typing import Dict, Any, List
import faiss
import json
import os

logger = logging.getLogger(__name__)

class InMemoryPipeline:
    """In-memory FAISS-based pipeline for fallback mode"""
    
    def __init__(self, embedder, vector_store):
        self.embedder = embedder
        self.vector_store = vector_store
        self.documents = []
        self.setup_pipeline()
        
    def setup_pipeline(self):
        """Setup in-memory FAISS index"""
        try:
            # Load existing documents if any
            data_file = "./data/processed_documents.json"
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    for line in f:
                        doc = json.loads(line.strip())
                        self.documents.append(doc)
                logger.info(f"📂 Loaded {len(self.documents)} existing documents")
            
            logger.info("✅ In-memory pipeline setup complete")
            
        except Exception as e:
            logger.error(f"❌ In-memory pipeline setup failed: {e}")
            raise
    
    def add_document(self, content: str, source: str, symbol: str = None) -> str:
        """Add document to in-memory pipeline"""
        try:
            doc_id = f"doc_{datetime.now().timestamp()}"
            embedding = self.embedder.embed(content)
            
            document = {
                "content": content,
                "embedding": embedding,
                "metadata": {
                    "source": source,
                    "symbol": symbol,
                    "timestamp": datetime.now().isoformat(),
                    "id": doc_id
                }
            }
            
            # Add to vector store
            self.vector_store.add_documents([document])
            self.documents.append(document)
            
            # Save to file for persistence
            with open("./data/processed_documents.json", "a") as f:
                f.write(json.dumps(document) + "\n")
            
            logger.info(f"📄 Document added to in-memory pipeline: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"❌ Failed to add document: {e}")
            raise
    
    def query(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Query the in-memory index"""
        try:
            return self.vector_store.search(query, k=k)
        except Exception as e:
            logger.error(f"❌ Query failed: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics"""
        return {
            "total_documents": len(self.documents),
            "pipeline_type": "in_memory",
            "status": "running"
        }