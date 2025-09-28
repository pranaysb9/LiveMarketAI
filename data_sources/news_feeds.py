"""
News Feed Source - Financial News and Articles
"""

import logging
import asyncio
import random
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class NewsFeedSource:
    """Source for financial news and articles"""
    
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.sources = ['Bloomberg', 'Reuters', 'CNBC', 'Financial Times', 'Wall Street Journal']
        self.categories = ['markets', 'stocks', 'crypto', 'economy', 'technology', 'earnings']
        self.is_running = False
        
    async def start_streaming(self):
        """Start streaming news feeds"""
        self.is_running = True
        logger.info("📰 Starting news feed stream")
        
        while self.is_running:
            try:
                # Generate simulated news articles
                news_articles = self._generate_news_articles()
                
                # Add to pipeline
                for article in news_articles:
                    self.pipeline.add_document(
                        content=article['content'],
                        source=article['source'],
                        symbol=article.get('symbol')
                    )
                
                logger.info(f"📝 Generated {len(news_articles)} news articles")
                await asyncio.sleep(15)  # New articles every 15 seconds
                
            except Exception as e:
                logger.error(f"❌ News feed streaming error: {e}")
                await asyncio.sleep(10)
    
    def _generate_news_articles(self) -> List[Dict[str, Any]]:
        """Generate simulated financial news articles"""
        articles = []
        current_time = datetime.now()
        
        # Generate 1-3 articles per cycle
        for _ in range(random.randint(1, 3)):
            source = random.choice(self.sources)
            category = random.choice(self.categories)
            symbol = random.choice(['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'BTC-USD', None])
            
            title = self._generate_headline(category, symbol)
            content = self._generate_article_content(title, category, symbol)
            
            articles.append({
                'title': title,
                'content': content,
                'source': source,
                'category': category,
                'symbol': symbol,
                'timestamp': current_time.isoformat()
            })
        
        return articles
    
    def _generate_headline(self, category: str, symbol: str = None) -> str:
        """Generate realistic news headline"""
        headlines = {
            'markets': [
                "Markets Show Mixed Signals Amid Economic Data",
                "Trading Volumes Surge as Investors React to Fed Comments",
                "Global Markets Navigate Currency Fluctuations"
            ],
            'stocks': [
                f"{symbol} Announces Strong Quarterly Results",
                f"Analysts Upgrade {symbol} Price Target",
                f"{symbol} Faces Regulatory Scrutiny Over Business Practices"
            ],
            'crypto': [
                "Cryptocurrency Market Sees Increased Institutional Interest",
                "Regulatory Clarity Boosts Digital Asset Prices",
                "Blockchain Adoption Grows Among Traditional Finance"
            ],
            'economy': [
                "Inflation Data Comes in Lower Than Expected",
                "Employment Figures Show Robust Job Growth",
                "Central Banks Coordinate on Monetary Policy"
            ],
            'technology': [
                "AI Innovation Drives Tech Sector Growth",
                "Cloud Computing Demand Exceeds Expectations",
                "Cybersecurity Concerns Rise With Digital Transformation"
            ],
            'earnings': [
                f"{symbol} Beats Earnings Expectations",
                f"{symbol} Revenue Growth Accelerates",
                f"{symbol} Provides Strong Forward Guidance"
            ]
        }
        
        category_headlines = headlines.get(category, headlines['markets'])
        return random.choice(category_headlines)
    
    def _generate_article_content(self, title: str, category: str, symbol: str = None) -> str:
        """Generate realistic article content"""
        templates = [
            f"{title}. Industry analysts are closely watching developments as market conditions evolve. "
            f"Recent data suggests changing investor sentiment across key sectors.",
            
            f"{title}. This development comes amid broader market movements and economic indicators "
            f"pointing to sustained growth in the sector.",
            
            f"{title}. The news has prompted reactions from major financial institutions, with several "
            f"adjusting their outlooks and investment recommendations accordingly."
        ]
        
        content = random.choice(templates)
        
        if symbol:
            content += f" The impact on {symbol} is being closely monitored by traders and analysts."
        
        # Add some realistic details
        details = [
            " Trading volumes have increased significantly over the past session.",
            " Market participants are evaluating the implications for portfolio strategy.",
            " This follows similar trends observed in international markets.",
            " Regulatory developments may influence future market direction."
        ]
        
        content += random.choice(details)
        return content
    
    def stop_streaming(self):
        """Stop news feed streaming"""
        self.is_running = False
        logger.info("🛑 News feed streaming stopped")
    
    def get_sources(self) -> List[str]:
        """Get list of news sources"""
        return self.sources.copy()