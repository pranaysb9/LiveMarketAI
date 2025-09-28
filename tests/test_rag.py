"""
Tests for RAG Components
"""

import pytest
import numpy as np
from backend.rag.embeddings import Embedder
from backend.rag.vector_store import VectorStore
from backend.rag.rag_engine import RAGEngine
from backend.in_memory_pipeline import InMemoryPipeline

def test_embedder_initialization():
    """Test embedder initialization"""
    embedder = Embedder()
    assert embedder is not None
    assert hasattr(embedder, 'embed')

def test_embedder_functionality():
    """Test embedder functionality"""
    embedder = Embedder()
    text = "Test financial market analysis"
    embedding = embedder.embed(text)
    
    assert isinstance(embedding, list)
    assert len(embedding) == embedder.dimension
    assert all(isinstance(x, float) for x in embedding)

def test_vector_store_initialization():
    """Test vector store initialization"""
    embedder = Embedder()
    vector_store = VectorStore(embedder)
    assert vector_store is not None
    assert hasattr(vector_store, 'add_documents')
    assert hasattr(vector_store, 'search')

def test_vector_store_operations():
    """Test vector store operations"""
    embedder = Embedder()
    vector_store = VectorStore(embedder)
    
    # Test adding documents
    test_docs = [
        {
            "content": "AAPL stock is performing well",
            "embedding": embedder.embed("AAPL stock is performing well"),
            "metadata": {"source": "test", "symbol": "AAPL"}
        },
        {
            "content": "Market trends show upward momentum",
            "embedding": embedder.embed("Market trends show upward momentum"),
            "metadata": {"source": "test", "symbol": None}
        }
    ]
    
    vector_store.add_documents(test_docs)
    stats = vector_store.get_stats()
    assert stats["total_documents"] == 2
    
    # Test search
    results = vector_store.search("AAPL performance", k=2)
    assert len(results) <= 2
    if results:
        assert "similarity_score" in results[0]

def test_rag_engine_initialization():
    """Test RAG engine initialization"""
    embedder = Embedder()
    vector_store = VectorStore(embedder)
    pipeline = InMemoryPipeline(embedder, vector_store)
    rag_engine = RAGEngine(pipeline, embedder, vector_store)
    
    assert rag_engine is not None
    assert hasattr(rag_engine, 'process_query')

def test_rag_engine_query_processing():
    """Test RAG engine query processing"""
    embedder = Embedder()
    vector_store = VectorStore(embedder)
    pipeline = InMemoryPipeline(embedder, vector_store)
    rag_engine = RAGEngine(pipeline, embedder, vector_store)
    
    # Add test document
    pipeline.add_document(
        content="The stock market shows strong performance in technology sector",
        source="test",
        symbol=None
    )
    
    # Process query
    result = rag_engine.process_query("How is the technology sector performing?")
    
    assert "answer" in result
    assert "sources" in result
    assert "confidence" in result
    assert "rag_metadata" in result

def test_retrieval_quality_metrics():
    """Test retrieval quality metrics calculation"""
    embedder = Embedder()
    vector_store = VectorStore(embedder)
    pipeline = InMemoryPipeline(embedder, vector_store)
    rag_engine = RAGEngine(pipeline, embedder, vector_store)
    
    # Test with empty results
    empty_docs = []
    result = rag_engine._enhance_response({"answer": "test"}, empty_docs)
    assert result["rag_metadata"]["retrieved_documents_count"] == 0
    assert result["rag_metadata"]["average_similarity_score"] == 0.0
    
    # Test with mock documents
    mock_docs = [
        {"similarity_score": 0.8, "metadata": {"source": "test1"}},
        {"similarity_score": 0.9, "metadata": {"source": "test2"}}
    ]
    result = rag_engine._enhance_response({"answer": "test"}, mock_docs)
    assert result["rag_metadata"]["average_similarity_score"] == 0.85
    assert result["rag_metadata"]["source_diversity"] == 2

def test_batch_operations():
    """Test batch operations"""
    embedder = Embedder()
    texts = [
        "First financial document",
        "Second market analysis",
        "Third investment report"
    ]
    
    embeddings = embedder.embed_batch(texts)
    assert len(embeddings) == 3
    assert all(len(emb) == embedder.dimension for emb in embeddings)