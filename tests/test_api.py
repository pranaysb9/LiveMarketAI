"""
API Tests for LiveMarket AI System
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from backend.api.app import app
from backend.main import livemarket_ai

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()

def test_system_status():
    """Test system status endpoint"""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "pipeline" in data
    assert "agents" in data
    assert "vector_store" in data

def test_query_endpoint():
    """Test query processing endpoint"""
    test_query = {
        "query": "What is the current market trend?",
        "context": {},
        "k": 3
    }
    
    response = client.post("/query", json=test_query)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert "confidence" in data

def test_document_addition():
    """Test document addition endpoint"""
    test_document = {
        "content": "Test document content about market analysis",
        "source": "test_source",
        "symbol": "TEST"
    }
    
    response = client.post("/documents", json=test_document)
    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data
    assert "status" in data

def test_document_count():
    """Test document count endpoint"""
    response = client.get("/documents/count")
    assert response.status_code == 200
    data = response.json()
    assert "document_count" in data
    assert isinstance(data["document_count"], int)

def test_invalid_query():
    """Test query with invalid data"""
    response = client.post("/query", json={"query": ""})
    # Should handle empty queries gracefully
    assert response.status_code in [200, 400]

@pytest.mark.asyncio
async def test_websocket_connection():
    """Test WebSocket connection"""
    from websockets import connect
    import json
    
    # This test requires the server to be running
    # In practice, you'd use TestClient for WebSocket testing
    pass

def test_error_handling():
    """Test error handling for malformed requests"""
    response = client.post("/query", json={"invalid": "data"})
    # Should return 422 for validation error
    assert response.status_code == 422

if __name__ == "__main__":
    pytest.main([__file__, "-v"])