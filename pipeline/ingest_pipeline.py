import asyncio
import logging
from datetime import datetime
from sqlalchemy import text
from scraper.makaut_scraper import scrape_source, get_source_health
from core.sources import URLS
from database.db import SessionLocal
from database.models import Notification, SystemFlag
from delivery.channel_broadcaster import broadcast_channel
from pipeline.message_formatter import format_message
from core.config import SCRAPE_INTERVAL, ADMIN_ID
from bot.telegram_app import get_bot

logger = logging.getLogger("PIPELINE")

async def start_pipeline():
    logger.info("🚀 ASYNC PIPELINE STARTED")
    while True:
        async with SessionLocal() as db: # Ensure proper session closing
            try:
                # Scrape Cycle
                for key, config in URLS.items():
                    items = await scrape_source(key, config)
                    for item in items:
                        # Fixed: Check existence without loading 5000 rows
                        exists = db.query(Notification.id).filter_by(content_hash=item['content_hash']).first()
                        if not exists:
                            notif = Notification(**item)
                            db.add(notif)
                            await db.commit()
                            await broadcast_channel([format_message(item)])
                    await asyncio.sleep(2)
                
                # Health Check
                health = get_source_health()
                for src, fails in health.items():
                    if fails >= 3:
                        await get_bot().send_message(ADMIN_ID, f"🚨 Source {src} is DOWN!")
                
            except Exception as e:
                logger.error(f"Pipeline Error: {e}")
                await db.rollback()
        
        await asyncio.sleep(int(SCRAPE_INTERVAL))