"""
Vector Store with FAISS for Efficient Similarity Search
"""

import logging
import numpy as np
import faiss
import json
import os
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class VectorStore:
    """FAISS-based vector store for efficient similarity search"""
    
    def __init__(self, embedder, dimension: int = None):
        self.embedder = embedder
        self.dimension = dimension or int(os.getenv('VECTOR_DIMENSION', '1536'))
        self.index = None
        self.documents = []
        self.setup_index()
        
    def setup_index(self):
        """Initialize or load FAISS index"""
        try:
            # Try to load existing index
            if os.path.exists('./data/vector_index.faiss'):
                self.index = faiss.read_index('./data/vector_index.faiss')
                # Load documents metadata
                if os.path.exists('./data/documents.json'):
                    with open('./data/documents.json', 'r') as f:
                        self.documents = json.load(f)
                logger.info(f"✅ Loaded existing index with {len(self.documents)} documents")
            else:
                # Create new index
                self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
                logger.info("✅ Created new FAISS index")
                
        except Exception as e:
            logger.error(f"❌ Index setup failed: {e}")
            # Create fallback index
            self.index = faiss.IndexFlatIP(self.dimension)
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to vector store"""
        try:
            if not documents:
                return
                
            # Extract embeddings
            embeddings = []
            valid_documents = []
            
            for doc in documents:
                if 'embedding' in doc:
                    embedding = doc['embedding']
                else:
                    embedding = self.embedder.embed(doc.get('content', ''))
                
                if len(embedding) == self.dimension:
                    embeddings.append(embedding)
                    valid_documents.append(doc)
            
            if not embeddings:
                return
                
            # Convert to numpy array
            embedding_matrix = np.array(embeddings).astype('float32')
            
            # Normalize for cosine similarity
            faiss.normalize_L2(embedding_matrix)
            
            # Add to index
            self.index.add(embedding_matrix)
            
            # Store documents metadata
            self.documents.extend(valid_documents)
            
            # Save index and documents
            self._persist_data()
            
            logger.info(f"📚 Added {len(valid_documents)} documents to vector store")
            
        except Exception as e:
            logger.error(f"❌ Failed to add documents: {e}")
    
    def search(self, query: str, k: int = 5, threshold: float = None) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        try:
            if threshold is None:
                threshold = float(os.getenv('SIMILARITY_THRESHOLD', 0.7))
                
            if not self.documents:
                return []
            
            # Generate query embedding
            query_embedding = self.embedder.embed(query)
            query_vector = np.array([query_embedding]).astype('float32')
            
            # Normalize for cosine similarity
            faiss.normalize_L2(query_vector)
            
            # Search
            scores, indices = self.index.search(query_vector, min(k, len(self.documents)))
            
            # Format results
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.documents) and score >= threshold:
                    doc = self.documents[idx]
                    results.append({
                        **doc,
                        "similarity_score": float(score)
                    })
            
            # Sort by score descending
            results.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            logger.info(f"🔍 Search found {len(results)} results for query: {query}")
            return results
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []
    
    def _persist_data(self):
        """Persist index and documents to disk"""
        try:
            # Create data directory if it doesn't exist
            os.makedirs('./data', exist_ok=True)
            
            # Save FAISS index
            faiss.write_index(self.index, './data/vector_index.faiss')
            
            # Save documents metadata
            with open('./data/documents.json', 'w') as f:
                json.dump(self.documents, f, indent=2)
                
        except Exception as e:
            logger.error(f"❌ Data persistence failed: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        return {
            "total_documents": len(self.documents),
            "index_size": self.index.ntotal if self.index else 0,
            "dimension": self.dimension,
            "storage_path": "./data/"
        }
    
    def clear(self):
        """Clear all documents from vector store"""
        try:
            self.index.reset()
            self.documents.clear()
            
            # Remove persisted files
            for file in ['./data/vector_index.faiss', './data/documents.json']:
                if os.path.exists(file):
                    os.remove(file)
            
            logger.info("🗑️ Vector store cleared")
            
        except Exception as e:
            logger.error(f"❌ Failed to clear vector store: {e}")