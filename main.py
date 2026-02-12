import asyncio
import logging
import sys

from core.logger import setup_logger
from database.init_db import init_db
from bot.telegram_app import start_telegram
from pipeline.ingest_pipeline import start_pipeline
from search_bot.search_app import start_search_bot 
from admin_bot.admin_app import start_admin_bot 

# Initialize Logger
setup_logger()
logger = logging.getLogger("MAIN")

async def main():
    """
    Main entry point for the TeleAcademic System.
    Orchestrates: 
    1. Broadcast Bot
    2. Search Bot
    3. Admin Bot
    4. Scraper Pipeline
    """
    logger.info("🚀 TELEACADEMIC TRIPLE-BOT SYSTEM STARTING")

    # 1. Database Initialization
    try:
        init_db()
        logger.info("DATABASE TABLES VERIFIED")
    except Exception as e:
        logger.critical(f"DATABASE INIT FAILED: {e}")
        sys.exit(1)

    # 2. Start Broadcast Bot (Primary Task)
    try:
        await start_telegram()
        logger.info("BROADCAST BOT INITIALIZED")
    except Exception as e:
        logger.critical(f"BROADCAST BOT START FAILED: {e}")
        sys.exit(1)

    # 3. Launch all background tasks
    logger.info("STARTING BACKGROUND SERVICES...")
    
    # Gathering tasks ensures the script stays alive until all tasks finish
    tasks = [
        asyncio.create_task(start_search_bot()),
        asyncio.create_task(start_admin_bot()),
        asyncio.create_task(start_pipeline())
    ]

    try:
        # The script will now wait for all tasks to complete or fail
        await asyncio.gather(*tasks)
    except Exception as e:
        logger.critical(f"SYSTEM CRITICAL FAILURE: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("SYSTEM SHUTDOWN BY USER")
        sys.exit(0)