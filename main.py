import asyncio
import logging
import sys

from core.logger import setup_logger
from database.init_db import init_db
from bot.telegram_app import start_telegram
from pipeline.ingest_pipeline import start_pipeline
from search_bot.search_app import start_search_bot 
from admin_bot.admin_app import start_admin_bot 
from group_bot.group_app import start_group_bot  # NEW: Group Monitor Import

# Initialize Logger [cite: 63, 64]
setup_logger()
logger = logging.getLogger("MAIN")

async def main():
    """
    Main entry point for the TeleAcademic System.
    Orchestrates the Quad-Bot architecture:
    1. Broadcast Bot (Main Channel) [cite: 78]
    2. Search Bot (Student Queries) [cite: 77]
    3. Admin Bot (System Management) [cite: 77]
    4. Group Bot (Ultra Supreme Monitoring)
    5. Scraper Pipeline (Date Forensic Engine) [cite: 77]
    """
    logger.info("🚀 TELEACADEMIC QUAD-BOT SYSTEM STARTING")

    # 1. Database Initialization [cite: 61]
    try:
        init_db()
        logger.info("DATABASE TABLES VERIFIED")
    except Exception as e:
        logger.critical(f"DATABASE INIT FAILED: {e}")
        sys.exit(1)

    # 2. Start Broadcast Bot (Primary Task) [cite: 78]
    try:
        await start_telegram()
        logger.info("BROADCAST BOT INITIALIZED")
    except Exception as e:
        logger.critical(f"BROADCAST BOT START FAILED: {e}")
        sys.exit(1)

    # 3. Launch all background tasks in parallel 
    logger.info("STARTING BACKGROUND SERVICES...")
    
    # Gathering tasks ensures the script stays alive until all services finish
    tasks = [
        asyncio.create_task(start_search_bot()),
        asyncio.create_task(start_admin_bot()),
        asyncio.create_task(start_pipeline()),
        asyncio.create_task(start_group_bot())  # NEW: Isolated Monitoring Task
    ]

    try:
        # The script waits for all tasks to complete or fail 
        await asyncio.gather(*tasks)
    except Exception as e:
        logger.critical(f"SYSTEM CRITICAL FAILURE: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Graceful shutdown for Linux Mint [cite: 80]
        logger.info("SYSTEM SHUTDOWN BY USER")
        sys.exit(0)