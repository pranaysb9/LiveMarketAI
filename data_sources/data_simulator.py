import asyncio
import logging

logger = logging.getLogger(__name__)

async def start_simulator():
    logger.info("📊 Data simulator started")
    while True:
        await asyncio.sleep(10)
