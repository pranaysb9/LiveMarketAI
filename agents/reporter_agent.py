"""
Financial Reporting AI Agent
"""

import logging
import os
from typing import Dict, Any, List
from openai import OpenAI

logger = logging.getLogger(__name__)

class ReporterAgent:
    """AI agent specialized in financial reporting and insights"""
    
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = os.getenv('MODEL_NAME', 'gpt-3.5-turbo')
        
    def generate_report(self, query: str, retrieved_docs: List[Dict], context: Dict = None) -> Dict[str, Any]:
        """Generate financial report based on query and context"""
        try:
            # Build comprehensive context
            context_text = self._build_reporting_context(retrieved_docs)
            
            system_prompt = """You are a financial reporter and analyst. Create insightful, 
            well-structured reports that synthesize information from multiple sources. 
            Focus on clarity, accuracy, and actionable insights."""
            
            user_prompt = f"""
            Query: {query}
            
            Available information:
            {context_text}
            
            Additional context: {context or 'None provided'}
            
            Please generate a comprehensive financial report that addresses the query.
            Structure your response with clear sections and bullet points where appropriate.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.4,
                max_tokens=800
            )
            
            report = response.choices[0].message.content
            
            return {
                "answer": report,
                "sources": [doc.get('metadata', {}) for doc in retrieved_docs],
                "confidence": self._calculate_report_confidence(retrieved_docs, report),
                "agent": "financial_reporter",
                "report_type": self._identify_report_type(query),
                "timestamp": self._get_timestamp()
            }
            
        except Exception as e:
            logger.error(f"❌ Report generation failed: {e}")
            raise
    
    def _build_reporting_context(self, retrieved_docs: List[Dict]) -> str:
        """Build structured context for reporting"""
        if not retrieved_docs:
            return "No relevant financial data available for reporting."
        
        # Group by source type for better organization
        news_sources = []
        market_sources = []
        other_sources = []
        
        for doc in retrieved_docs:
            metadata = doc.get('metadata', {})
            source = metadata.get('source', 'unknown')
            content = doc.get('content', '')
            
            if 'news' in source.lower() or 'article' in source.lower():
                news_sources.append(f"- {content} (Source: {source})")
            elif 'market' in source.lower() or 'price' in source.lower():
                market_sources.append(f"- {content} (Symbol: {metadata.get('symbol', 'N/A')})")
            else:
                other_sources.append(f"- {content} (Source: {source})")
        
        context_parts = []
        if news_sources:
            context_parts.append("NEWS AND ARTICLES:")
            context_parts.extend(news_sources)
            context_parts.append("")
        
        if market_sources:
            context_parts.append("MARKET DATA:")
            context_parts.extend(market_sources)
            context_parts.append("")
        
        if other_sources:
            context_parts.append("OTHER SOURCES:")
            context_parts.extend(other_sources)
        
        return "\n".join(context_parts)
    
    def _calculate_report_confidence(self, retrieved_docs: List[Dict], report: str) -> float:
        """Calculate confidence score for the report"""
        if not retrieved_docs:
            return 0.4
        
        base_confidence = min(0.6 + (len(retrieved_docs) * 0.05), 0.9)
        
        # Adjust based on report structure and completeness
        structure_indicators = ['summary', 'analysis', 'conclusion', 'recommendation']
        found_indicators = sum(1 for indicator in structure_indicators 
                             if indicator in report.lower())
        
        base_confidence += found_indicators * 0.05
        
        return min(base_confidence, 1.0)
    
    def _identify_report_type(self, query: str) -> str:
        """Identify the type of report being requested"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['summary', 'overview']):
            return "executive_summary"
        elif any(word in query_lower for word in ['analysis', 'analyze']):
            return "detailed_analysis"
        elif any(word in query_lower for word in ['forecast', 'prediction']):
            return "forecast"
        elif any(word in query_lower for word in ['news', 'update']):
            return "news_report"
        else:
            return "general_report"
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def generate_daily_briefing(self) -> Dict[str, Any]:
        """Generate automated daily market briefing"""
        try:
            # Query for recent market data and news
            market_docs = self.pipeline.query("stock market today news prices", k=15)
            
            briefing = self.generate_report(
                "Generate a comprehensive daily market briefing covering major indices, "
                "notable stock movements, key news events, and market outlook for today",
                market_docs
            )
            
            return {
                **briefing,
                "briefing_type": "daily_market_briefing",
                "automated": True
            }
            
        except Exception as e:
            logger.error(f"❌ Daily briefing generation failed: {e}")
            return {
                "answer": "Unable to generate daily briefing at this time.",
                "sources": [],
                "confidence": 0.0,
                "error": str(e)
            }