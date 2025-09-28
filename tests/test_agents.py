"""
Tests for AI Agents
"""

import pytest
from backend.agents.market_agent import MarketAgent
from backend.agents.reporter_agent import ReporterAgent
from backend.in_memory_pipeline import InMemoryPipeline
from backend.rag.embeddings import Embedder
from backend.rag.vector_store import VectorStore

@pytest.fixture
def setup_components():
    """Setup test components"""
    embedder = Embedder()
    vector_store = VectorStore(embedder)
    pipeline = InMemoryPipeline(embedder, vector_store)
    return embedder, vector_store, pipeline

def test_market_agent_initialization(setup_components):
    """Test market agent initialization"""
    embedder, vector_store, pipeline = setup_components
    agent = MarketAgent(pipeline)
    assert agent is not None
    assert hasattr(agent, 'analyze')

def test_reporter_agent_initialization(setup_components):
    """Test reporter agent initialization"""
    embedder, vector_store, pipeline = setup_components
    agent = ReporterAgent(pipeline)
    assert agent is not None
    assert hasattr(agent, 'generate_report')

def test_market_agent_analysis(setup_components):
    """Test market agent analysis"""
    embedder, vector_store, pipeline = setup_components
    agent = MarketAgent(pipeline)
    
    # Add test document
    pipeline.add_document(
        content="AAPL stock is showing strong upward momentum with increased trading volume",
        source="test",
        symbol="AAPL"
    )
    
    # Test analysis
    retrieved_docs = pipeline.query("AAPL stock performance", k=3)
    result = agent.analyze("How is AAPL performing?", retrieved_docs)
    
    assert "answer" in result
    assert "sources" in result
    assert "confidence" in result
    assert isinstance(result["confidence"], float)

def test_reporter_agent_report(setup_components):
    """Test reporter agent report generation"""
    embedder, vector_store, pipeline = setup_components
    agent = ReporterAgent(pipeline)
    
    # Add test documents
    pipeline.add_document(
        content="Market shows mixed signals with technology sector outperforming",
        source="test_news",
        symbol=None
    )
    
    # Test report generation
    retrieved_docs = pipeline.query("market analysis", k=3)
    result = agent.generate_report("Market overview", retrieved_docs)
    
    assert "answer" in result
    assert "sources" in result
    assert "confidence" in result
    assert "report_type" in result

def test_confidence_calculation(setup_components):
    """Test confidence score calculation"""
    embedder, vector_store, pipeline = setup_components
    agent = MarketAgent(pipeline)
    
    # Test with empty documents
    empty_docs = []
    result = agent.analyze("test query", empty_docs)
    assert result["confidence"] == 0.3  # Base confidence for no docs
    
    # Test with documents
    pipeline.add_document("test content", "test_source", "TEST")
    docs = pipeline.query("test", k=1)
    result = agent.analyze("test query", docs)
    assert 0.3 <= result["confidence"] <= 1.0

def test_signal_generation(setup_components):
    """Test trading signal generation"""
    embedder, vector_store, pipeline = setup_components
    agent = MarketAgent(pipeline)
    
    # Add relevant document
    pipeline.add_document(
        content="AAPL shows strong buy signals with breaking resistance levels",
        source="technical_analysis",
        symbol="AAPL"
    )
    
    signal = agent.generate_trading_signal("AAPL")
    assert "symbol" in signal
    assert "signal_type" in signal
    assert signal["symbol"] == "AAPL"
    assert signal["signal_type"] in ["BUY", "SELL", "HOLD"]