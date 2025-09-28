"""
Market Data Source - Real-time Financial Data
"""

import logging
import asyncio
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class MarketDataSource:
    """Source for real-time market data"""
    
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'META', 'NVDA', 'BTC-USD', 'ETH-USD']
        self.is_running = False
        
    async def start_streaming(self):
        """Start streaming market data"""
        self.is_running = True
        logger.info("📊 Starting market data stream")
        
        while self.is_running:
            try:
                # Simulate market data updates
                market_data = self._generate_market_data()
                
                # Convert to document format and add to pipeline
                for symbol, data in market_data.items():
                    content = self._format_market_content(symbol, data)
                    self.pipeline.add_document(
                        content=content,
                        source="market_data",
                        symbol=symbol
                    )
                
                logger.info(f"📈 Generated market data for {len(market_data)} symbols")
                await asyncio.sleep(10)  # Update every 10 seconds
                
            except Exception as e:
                logger.error(f"❌ Market data streaming error: {e}")
                await asyncio.sleep(5)
    
    def _generate_market_data(self) -> Dict[str, Dict[str, Any]]:
        """Generate simulated market data"""
        import random
        import time
        
        data = {}
        current_time = datetime.now()
        
        for symbol in self.symbols:
            base_price = {
                'AAPL': 180, 'GOOGL': 130, 'MSFT': 330, 'TSLA': 240, 
                'AMZN': 145, 'META': 320, 'NVDA': 480, 'BTC-USD': 42000, 'ETH-USD': 2200
            }.get(symbol, 100)
            
            # Generate realistic price movement
            change_percent = random.uniform(-2.0, 2.0)
            price = base_price * (1 + change_percent / 100)
            change = price - base_price
            
            volume = random.randint(1000000, 50000000)
            
            data[symbol] = {
                'symbol': symbol,
                'price': round(price, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'volume': volume,
                'timestamp': current_time.isoformat(),
                'market_cap': random.randint(100000000000, 3000000000000)
            }
        
        return data
    
    def _format_market_content(self, symbol: str, data: Dict[str, Any]) -> str:
        """Format market data as text content"""
        trend = "up" if data['change'] > 0 else "down"
        return (
            f"{symbol} is trading at ${data['price']}, {trend} {abs(data['change_percent'])}% "
            f"({'+' if data['change'] > 0 else ''}{data['change']}). "
            f"Volume: {data['volume']:,}. Market cap: ${data['market_cap']:,}. "
            f"Latest update: {data['timestamp']}"
        )
    
    def stop_streaming(self):
        """Stop market data streaming"""
        self.is_running = False
        logger.info("🛑 Market data streaming stopped")
    
    def get_available_symbols(self) -> List[str]:
        """Get list of available symbols"""
        return self.symbols.copy()