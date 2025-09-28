#!/usr/bin/env python3
"""
LiveMarket AI - Main Entry Point
"""

import asyncio
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    try:
        logger.info("🚀 Starting LiveMarket AI System")
        
        from backend.api.app import app
        from backend.data_sources.data_simulator import start_simulator
        from backend.api.websocket import websocket_manager
        
        if os.getenv('SIMULATOR_ENABLED', 'true').lower() == 'true':
            asyncio.create_task(start_simulator())
            logger.info("�� Data simulator started")
        
        if os.getenv('WEBSOCKET_ENABLED', 'true').lower() == 'true':
            asyncio.create_task(websocket_manager.start())
            logger.info("🔌 WebSocket manager started")
        
        import uvicorn
        port = int(os.getenv('PORT', 8000))
        logger.info(f"🌐 Starting server on port {port}")
        
        config = uvicorn.Config(
            app, 
            host="0.0.0.0", 
            port=port,
            reload=False,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()
        
    except Exception as e:
        logger.error(f"❌ Failed to start application: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
