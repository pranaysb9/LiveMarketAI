"""
REAL OpenAI Market Agent - Uses actual GPT API
"""

import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class RealMarketAgent:
    """Actual OpenAI-powered market analyst"""
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_actual_openai_key_here':
            self.client = None
            self.valid_key = False
            logger.warning("❌ No valid OpenAI API key found. Using fallback mode.")
        else:
            self.client = OpenAI(api_key=api_key)
            self.valid_key = True
            logger.info("✅ OpenAI client initialized with real API key")
    
    async def analyze(self, query, market_data=None, context=None):
        """Use REAL OpenAI API for market analysis"""
        
        # If no valid API key, use fallback
        if not self.valid_key or not self.client:
            return await self._fallback_analysis(query, market_data)
        
        try:
            # Prepare market context from real data
            market_context = self._build_market_context(market_data)
            
            # Create system prompt for financial analysis
            system_prompt = """You are a senior financial market analyst at a top investment firm. 
            Provide accurate, insightful market analysis based on the provided context.
            Be specific about trends, risks, and opportunities. Always maintain professional tone.
            If specific data is provided, reference it directly in your analysis."""
            
            user_prompt = f"""
            Query: {query}
            
            Current Market Context:
            {market_context}
            
            Additional Context: {context or 'None provided'}
            
            Please provide a comprehensive market analysis addressing the query.
            Focus on actionable insights and current market conditions.
            """
            
            # Make REAL API call to OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            
            return {
                "answer": answer,
                "sources": ["OpenAI GPT-3.5-Turbo", "Live Market Data", "Financial Analysis"],
                "confidence": 0.92,
                "agent": "openai_market_analyst",
                "real_ai": True,
                "api_used": "OpenAI GPT-3.5-Turbo"
            }
            
        except Exception as e:
            logger.error(f"❌ OpenAI API call failed: {e}")
            # Fallback to basic analysis
            return await self._fallback_analysis(query, market_data)
    
    def _build_market_context(self, market_data):
        """Build context string from real market data"""
        if not market_data:
            return "No specific market data available. Provide general market analysis."
        
        context_parts = ["Current Market Data:"]
        for item in market_data[:8]:  # Limit to 8 items
            symbol = item.get('symbol', 'Unknown')
            price = item.get('price', 0)
            change = item.get('change', 0)
            change_percent = item.get('change_percent', 0)
            
            context_parts.append(
                f"{symbol}: ${price} ({change:+.2f}, {change_percent:+.2f}%)"
            )
        
        return "\n".join(context_parts)
    
    async def _fallback_analysis(self, query, market_data):
        """Fallback analysis when no OpenAI API available"""
        query_lower = query.lower()
        
        # Basic pattern matching for common queries
        if any(word in query_lower for word in ['apple', 'aapl']):
            return {
                "answer": "📈 **Apple Inc. (AAPL) - Basic Analysis**\n\n• **Status:** Large-cap technology stock\n• **Focus:** Consumer electronics, services\n• **Market:** NASDAQ listed\n• **Note:** For detailed AI analysis, please add your OpenAI API key to .env file\n\n*Enable OpenAI API for advanced AI-powered analysis*",
                "sources": ["Basic Market Data", "Public Information"],
                "confidence": 0.7,
                "agent": "basic_analyst",
                "real_ai": False,
                "api_used": "None - API key required"
            }
        elif any(word in query_lower for word in ['bitcoin', 'crypto', 'btc']):
            return {
                "answer": "₿ **Bitcoin (BTC) - Basic Analysis**\n\n• **Asset Class:** Cryptocurrency\n• **Market:** 24/7 digital asset trading\n• **Volatility:** Typically high\n• **Note:** Add OpenAI API key for AI-powered crypto analysis\n\n*Real-time price data is active, but AI analysis requires API key*",
                "sources": ["Crypto Market Data", "Basic Analysis"],
                "confidence": 0.7,
                "agent": "basic_analyst", 
                "real_ai": False,
                "api_used": "None - API key required"
            }
        else:
            return {
                "answer": f"🤖 **Market Analysis - Basic Mode**\n\nI've received your query about '{query}'. \n\n**To enable AI-powered analysis:**\n1. Get an OpenAI API key from https://platform.openai.com/api-keys\n2. Add it to your .env file as OPENAI_API_KEY=your_key_here\n3. Restart the backend server\n\n**Current Features Active:**\n✅ Real-time stock prices (Yahoo Finance)\n✅ Live cryptocurrency data (CoinGecko)\n✅ Basic market data processing\n\n**Waiting for AI Enablement:**\n🔒 Advanced AI analysis (OpenAI API)\n🔒 Intelligent market insights\n🔒 Predictive analytics",
                "sources": ["System Information", "Market Data Feeds"],
                "confidence": 0.6,
                "agent": "basic_analyst",
                "real_ai": False,
                "api_used": "None - API key required"
            }

# Global instance
real_market_agent = RealMarketAgent()
