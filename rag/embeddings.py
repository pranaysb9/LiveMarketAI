"""
Embedding Service with OpenAI and Local Fallback
"""

import os
import logging
import numpy as np
from typing import List
from openai import OpenAI

logger = logging.getLogger(__name__)

class Embedder:
    """Unified embedding service with multiple providers"""
    
    def __init__(self):
        self.embedder_type = os.getenv('EMBEDDER_TYPE', 'openai').lower()
        self.dimension = int(os.getenv('VECTOR_DIMENSION', 
                                     '1536' if self.embedder_type == 'openai' else '384'))
        
        if self.embedder_type == 'openai':
            self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            logger.info("✅ Using OpenAI embeddings")
        else:
            try:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("✅ Using local sentence-transformers embeddings")
            except ImportError:
                logger.warning("❌ sentence-transformers not available, falling back to random embeddings")
                self.model = None
    
    def embed(self, text: str) -> List[float]:
        """Generate embedding for text"""
        try:
            if self.embedder_type == 'openai':
                return self._openai_embed(text)
            else:
                return self._local_embed(text)
        except Exception as e:
            logger.error(f"❌ Embedding failed: {e}")
            # Return random embedding as fallback
            return list(np.random.normal(0, 0.1, self.dimension))
    
    def _openai_embed(self, text: str) -> List[float]:
        """Generate embedding using OpenAI"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"❌ OpenAI embedding failed: {e}")
            raise
    
    def _local_embed(self, text: str) -> List[float]:
        """Generate embedding using local model"""
        if self.model is None:
            # Fallback to random embeddings
            return list(np.random.normal(0, 0.1, self.dimension))
        
        try:
            embedding = self.model.encode([text])[0]
            return embedding.tolist()
        except Exception as e:
            logger.error(f"❌ Local embedding failed: {e}")
            # Fallback to random
            return list(np.random.normal(0, 0.1, self.dimension))
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        try:
            if self.embedder_type == 'openai':
                return self._openai_embed_batch(texts)
            else:
                return self._local_embed_batch(texts)
        except Exception as e:
            logger.error(f"❌ Batch embedding failed: {e}")
            return [list(np.random.normal(0, 0.1, self.dimension)) for _ in texts]
    
    def _openai_embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate batch embeddings using OpenAI"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"❌ OpenAI batch embedding failed: {e}")
            raise
    
    def _local_embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate batch embeddings using local model"""
        if self.model is None:
            return [list(np.random.normal(0, 0.1, self.dimension)) for _ in texts]
        
        try:
            embeddings = self.model.encode(texts)
            return [embedding.tolist() for embedding in embeddings]
        except Exception as e:
            logger.error(f"❌ Local batch embedding failed: {e}")
            return [list(np.random.normal(0, 0.1, self.dimension)) for _ in texts]