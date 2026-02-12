import asyncio
import logging
import os
from datetime import datetime

from scraper.makaut_scraper import scrape_source
from core.sources import URLS
from database.db import SessionLocal
from database.models import Notification, SystemFlag
from delivery.channel_broadcaster import broadcast_channel
from pipeline.message_formatter import format_message
from core.config import SCRAPE_INTERVAL

logger = logging.getLogger("PIPELINE")

FIRST_BOOT_LIMIT = 20
HASH_CACHE_LIMIT = 5000

async def start_pipeline():
    """
    Main background task for the notification pipeline.
    Orchestrates: Scraping -> Chronological Sorting -> De-duplication -> Delivery -> Storage.
    """
    logger.info("PIPELINE STARTED")
    await asyncio.sleep(5)

    while True:
        db = None
        try:
            logger.info("SCRAPE CYCLE START")
            
            all_scraped_items = []
            
            # --- GLOBAL THROTTLER LOGIC (AI-FREE OPTIMIZED) ---
            # Scrape each university source one by one.
            for key, config in URLS.items():
                logger.info(f"SCRAPING SOURCE: {key}")
                source_data = scrape_source(key, config)
                all_scraped_items.extend(source_data)
                
                # Reduced to 2 seconds because Gemini 429 errors are no longer a risk.
                # This keeps the bot fast but polite to university servers.
                await asyncio.sleep(2) 

            if not all_scraped_items:
                logger.info("No 2026 items found in this cycle.")
                await asyncio.sleep(int(SCRAPE_INTERVAL))
                continue

            # --- CHRONOLOGICAL SORT ---
            # Sort items by published_date (Oldest to Newest).
            all_scraped_items.sort(key=lambda x: x['published_date'])

            db = SessionLocal()

            # Load recent hashes to prevent duplicates
            existing_hashes = {
                h for (h,) in db.query(Notification.content_hash)
                .order_by(Notification.id.desc())
                .limit(HASH_CACHE_LIMIT)
                .all()
            }

            new_notifications = []
            notifications_to_save = []

            for item in all_scraped_items:
                h = item.get("content_hash")
                if not h or h in existing_hashes:
                    continue

                notif = Notification(**item)
                notifications_to_save.append(notif)
                new_notifications.append(item)
                existing_hashes.add(h)

            logger.info(f"NEW 2026 NOTIFICATIONS DISCOVERED: {len(new_notifications)}")

            if not new_notifications:
                db.close()
                await asyncio.sleep(int(SCRAPE_INTERVAL))
                continue

            # Check for first-run status to avoid massive spam on initial deployment
            first_flag = db.query(SystemFlag).filter_by(key="FIRST_RUN_DONE").first()
            
            msgs_to_send = []
            if not first_flag:
                logger.info("FIRST BOOT MODE ACTIVE - LIMITING BROADCAST")
                limited_items = new_notifications[:FIRST_BOOT_LIMIT]
                msgs_to_send = [format_message(n) for n in limited_items]
                db.add(SystemFlag(key="FIRST_RUN_DONE", value="1"))
            else:
                msgs_to_send = [format_message(n) for n in new_notifications]

            # 1. BROADCAST FIRST
            if msgs_to_send:
                await broadcast_channel(msgs_to_send)

            # 2. SAVE TO DB AFTER SUCCESSFUL SENDING
            for n_obj in notifications_to_save:
                db.add(n_obj)
            
            db.commit()
            logger.info("DATABASE SYNC COMPLETE")

        except Exception as e:
            logger.error(f"PIPELINE ERROR: {e}", exc_info=True)
            if db: db.rollback()
        finally:
            if db: db.close()

        logger.info(f"SCRAPE CYCLE DONE. Sleeping for {SCRAPE_INTERVAL}s")
        await asyncio.sleep(int(SCRAPE_INTERVAL))