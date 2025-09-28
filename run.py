#!/usr/bin/env python3
"""
LiveMarket AI - PURE REAL DATA BOT
No hardcoded text - just raw market data and real analysis
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import asyncio
import aiohttp
import yfinance as yf
from datetime import datetime, timedelta
from dotenv import load_dotenv
import random

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LiveMarket AI - PURE DATA",
    description="Raw market data and real analysis - no hardcoded text",
    version="10.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REAL Market Data Class
class RealMarketData:
    def __init__(self):
        self.symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'META', 'NVDA', 'BTC-USD', 'ETH-USD']
        self.cache = {}
        self.cache_timeout = 15  # More frequent updates
    
    async def get_yahoo_finance_realtime(self, symbol):
        """Get ACTUAL real-time data using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            current_price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose')
            previous_close = info.get('previousClose', current_price)
            
            if current_price and previous_close:
                change = current_price - previous_close
                change_percent = (change / previous_close) * 100
                
                return {
                    'symbol': symbol,
                    'price': round(current_price, 2),
                    'change': round(change, 2),
                    'change_percent': round(change_percent, 2),
                    'previous_close': round(previous_close, 2),
                    'volume': info.get('volume', 0),
                    'timestamp': datetime.now().isoformat(),
                    'data_source': 'YAHOO_FINANCE_REAL'
                }
            return None
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return None
    
    async def get_crypto_realtime(self, symbol):
        """Get ACTUAL cryptocurrency data"""
        try:
            coin_id = symbol.lower().replace('-usd', '')
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        if coin_id in data:
                            coin_data = data[coin_id]
                            price = coin_data.get('usd', 0)
                            change_percent = coin_data.get('usd_24h_change', 0)
                            change = (price * change_percent) / 100
                            
                            return {
                                'symbol': symbol,
                                'price': round(price, 2),
                                'change': round(change, 2),
                                'change_percent': round(change_percent, 2),
                                'timestamp': datetime.now().isoformat(),
                                'data_source': 'COINGECKO_REAL'
                            }
            return None
        except Exception as e:
            logger.error(f"Error fetching crypto data for {symbol}: {e}")
            return None
    
    async def get_all_market_data(self):
        """Get ACTUAL market data for all symbols"""
        current_time = datetime.now()
        
        if (self.cache.get('timestamp') and 
            current_time - self.cache['timestamp'] < timedelta(seconds=self.cache_timeout)):
            return self.cache['data']
        
        results = []
        
        tasks = []
        for symbol in self.symbols:
            if '-USD' in symbol.upper():
                tasks.append(self.get_crypto_realtime(symbol))
            else:
                tasks.append(self.get_yahoo_finance_realtime(symbol))
        
        data_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in data_results:
            if isinstance(result, dict) and result:
                results.append(result)
        
        self.cache = {
            'timestamp': current_time,
            'data': results
        }
        
        return results

real_data = RealMarketData()

# PURE DATA Analysis Bot - No Hardcoded Text
class PureDataBot:
    """Analyzes real market data and generates responses from scratch"""
    
    async def analyze(self, query, market_data=None):
        """Generate responses purely from real data analysis"""
        if not market_data:
            market_data = await real_data.get_all_market_data()
        
        query_lower = query.lower()
        current_time = datetime.now()
        
        # Extract symbols from query
        symbols_in_query = []
        for item in market_data:
            if item['symbol'].lower().replace('-usd', '') in query_lower:
                symbols_in_query.append(item['symbol'])
        
        if symbols_in_query:
            return await self._analyze_symbols(symbols_in_query, market_data, query, current_time)
        else:
            return await self._analyze_market(market_data, query, current_time)
    
    async def _analyze_symbols(self, symbols, market_data, query, current_time):
        """Analyze specific symbols"""
        symbol_data = []
        for symbol in symbols:
            data = next((item for item in market_data if item['symbol'] == symbol), None)
            if data:
                symbol_data.append(data)
        
        if not symbol_data:
            return await self._analyze_market(market_data, query, current_time)
        
        # Build response from pure data analysis
        response_lines = []
        
        for data in symbol_data:
            # Calculate metrics from real data
            volatility = self._calculate_volatility(data, market_data)
            performance = self._calculate_performance(data)
            trend = self._calculate_trend(data)
            
            line = f"{data['symbol']}: ${data['price']} "
            if data['change'] >= 0:
                line += f"(+${data['change']:.2f}, +{data['change_percent']:.2f}%)"
            else:
                line += f"(-${abs(data['change']):.2f}, {data['change_percent']:.2f}%)"
            
            line += f" | Vol: {data['volume']:,}"
            line += f" | Trend: {trend}"
            line += f" | Perf: {performance}"
            
            response_lines.append(line)
        
        answer = "Live Market Data:\n" + "\n".join(response_lines)
        answer += f"\n\nUpdated: {current_time.strftime('%H:%M:%S')}"
        answer += f" | Sources: {', '.join(set([d['data_source'] for d in symbol_data]))}"
        
        # Calculate confidence based on data freshness and completeness
        confidence = min(0.95, 0.7 + (len(symbol_data) * 0.05))
        
        return {
            "answer": answer,
            "sources": list(set([d['data_source'] for d in symbol_data])),
            "confidence": round(confidence, 2),
            "agent": "data_analyzer",
            "metrics": {
                "symbols_analyzed": len(symbol_data),
                "data_points": len(symbol_data) * 6,  # price, change, %, volume, etc.
                "analysis_time": current_time.isoformat()
            }
        }
    
    async def _analyze_market(self, market_data, query, current_time):
        """Analyze overall market"""
        if not market_data:
            return {
                "answer": "No market data available",
                "sources": [],
                "confidence": 0.0,
                "agent": "system"
            }
        
        # Calculate real market metrics
        total_assets = len(market_data)
        advancing = len([d for d in market_data if d['change_percent'] > 0])
        declining = len([d for d in market_data if d['change_percent'] < 0])
        unchanged = total_assets - advancing - declining
        
        # Calculate average performance
        avg_change = sum(d['change_percent'] for d in market_data) / total_assets
        total_volume = sum(d.get('volume', 0) for d in market_data if d.get('volume'))
        
        # Find extremes
        top_gainers = sorted(market_data, key=lambda x: x['change_percent'], reverse=True)[:3]
        top_losers = sorted(market_data, key=lambda x: x['change_percent'])[:3]
        
        # Build response from pure calculations
        response_lines = [
            f"Market Summary - {current_time.strftime('%H:%M:%S')}",
            f"Assets: {total_assets} | Advancing: {advancing} | Declining: {declining} | Unchanged: {unchanged}",
            f"Avg Change: {avg_change:+.2f}% | Total Volume: {total_volume:,}",
            "",
            "Top Gainers:"
        ]
        
        for gainer in top_gainers:
            response_lines.append(f"  {gainer['symbol']}: +{gainer['change_percent']:.2f}% (${gainer['price']})")
        
        response_lines.append("")
        response_lines.append("Top Losers:")
        
        for loser in top_losers:
            response_lines.append(f"  {loser['symbol']}: {loser['change_percent']:.2f}% (${loser['price']})")
        
        response_lines.append("")
        response_lines.append(f"Data Sources: {', '.join(set(d['data_source'] for d in market_data))}")
        
        answer = "\n".join(response_lines)
        
        # Confidence based on data quality
        confidence = min(0.92, 0.6 + (len(market_data) * 0.03))
        
        return {
            "answer": answer,
            "sources": list(set(d['data_source'] for d in market_data)),
            "confidence": round(confidence, 2),
            "agent": "market_analyzer",
            "metrics": {
                "total_assets": total_assets,
                "market_sentiment": "positive" if avg_change > 0 else "negative",
                "volatility_index": self._calculate_market_volatility(market_data),
                "analysis_timestamp": current_time.isoformat()
            }
        }
    
    def _calculate_volatility(self, symbol_data, market_data):
        """Calculate volatility based on price movement"""
        change_abs = abs(symbol_data['change_percent'])
        if change_abs > 5:
            return "high"
        elif change_abs > 2:
            return "medium"
        else:
            return "low"
    
    def _calculate_performance(self, symbol_data):
        """Calculate performance rating"""
        change = symbol_data['change_percent']
        if change > 3:
            return "strong"
        elif change > 1:
            return "good"
        elif change > -1:
            return "neutral"
        elif change > -3:
            return "weak"
        else:
            return "poor"
    
    def _calculate_trend(self, symbol_data):
        """Calculate trend direction"""
        if symbol_data['change_percent'] > 1:
            return "up"
        elif symbol_data['change_percent'] < -1:
            return "down"
        else:
            return "flat"
    
    def _calculate_market_volatility(self, market_data):
        """Calculate overall market volatility"""
        changes = [abs(d['change_percent']) for d in market_data]
        avg_volatility = sum(changes) / len(changes) if changes else 0
        return round(avg_volatility, 2)

market_bot = PureDataBot()

@app.get("/")
async def root():
    return {
        "message": "LiveMarket AI - PURE DATA BOT",
        "version": "10.0.0",
        "status": "active",
        "data_mode": "REAL_TIME_ANALYSIS",
        "features": ["Pure Data Analysis", "No Hardcoded Text", "Real Calculations"],
        "analysis_types": ["symbol_analysis", "market_analysis", "performance_metrics"]
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "pure_data_bot",
        "timestamp": datetime.now().isoformat(),
        "data_sources": ["Yahoo Finance", "CoinGecko"]
    }

@app.get("/market/data")
async def get_market_data():
    """Returns ACTUAL real market data"""
    live_data = await real_data.get_all_market_data()
    return {
        "timestamp": datetime.now().isoformat(),
        "data": live_data,
        "update_frequency": "15 seconds",
        "data_source": "LIVE_FINANCIAL_APIS",
        "assets_covered": len(live_data),
        "raw_data": True
    }

@app.get("/analysis/metrics")
async def get_analysis_metrics():
    """Show current analysis metrics"""
    market_data = await real_data.get_all_market_data()
    
    if not market_data:
        return {"error": "No data available"}
    
    # Calculate real metrics
    total_assets = len(market_data)
    avg_change = sum(d['change_percent'] for d in market_data) / total_assets
    total_volume = sum(d.get('volume', 0) for d in market_data if d.get('volume'))
    
    return {
        "timestamp": datetime.now().isoformat(),
        "total_assets": total_assets,
        "average_change": round(avg_change, 2),
        "total_volume": total_volume,
        "data_sources": list(set(d['data_source'] for d in market_data)),
        "analysis_capabilities": [
            "real_time_price_analysis",
            "performance_calculations", 
            "volatility_metrics",
            "market_sentiment",
            "volume_analysis"
        ]
    }

@app.post("/query")
async def process_query(request: dict):
    query = request.get('query', '').strip()
    
    if not query:
        return {
            "answer": "Please provide a market-related question",
            "confidence": 0.0,
            "sources": [],
            "status": "error"
        }
    
    try:
        # Get REAL market data
        current_market_data = await real_data.get_all_market_data()
        
        # Use PURE DATA bot (no hardcoded responses)
        response = await market_bot.analyze(query, current_market_data)
        
        return {
            "answer": response["answer"],
            "sources": response["sources"],
            "confidence": response["confidence"],
            "agent": response["agent"],
            "timestamp": datetime.now().isoformat(),
            "metrics": response.get("metrics", {}),
            "status": "success"
        }
        
    except Exception as e:
        return {
            "answer": f"Data analysis error: {str(e)}",
            "confidence": 0.0,
            "sources": [],
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    print("=" * 70)
    print("�� LIVE MARKET AI - PURE DATA BOT")
    print("📍 Backend URL: http://localhost:8000")
    print("📊 Data: Pure market data from Yahoo Finance & CoinGecko")
    print("🔍 Analysis: Real calculations - No hardcoded text")
    print("📈 Metrics: Live performance, volatility, trends")
    print("=" * 70)
    print("")
    print("💡 This bot:")
    print("• Shows RAW market data numbers")
    print("• Calculates REAL metrics from data")  
    print("• No pre-written responses")
    print("• Pure data analysis")
    print("")
    print("🔍 Try these:")
    print("• 'AAPL' - Raw Apple data with calculations")
    print("• 'Market' - Real market metrics") 
    print("• 'BTC TSLA' - Multiple symbols analysis")
    print("")
    print("=" * 70)
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        access_log=True
    )
