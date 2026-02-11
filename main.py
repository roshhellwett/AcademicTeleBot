import asyncio
import logging

from database.init_db import init_db
from bot.telegram_app import init_telegram, start_telegram, get_bot
from pipeline.ingest_pipeline import start_pipeline


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("MAIN")


async def main():

    logger.info("🚀 TELEACADEMIC BOT STARTING")

    # ===== INIT DATABASE =====
    init_db()
    logger.info("DATABASE READY")

    # ===== INIT TELEGRAM (BUILD APP) =====
    await init_telegram()

    # ===== START TELEGRAM =====
    await start_telegram()

    logger.info("TELEGRAM READY")

    # ===== START PIPELINE AFTER TELEGRAM READY =====
    asyncio.create_task(start_pipeline())

    logger.info("PIPELINE BACKGROUND TASK STARTED")

    # ===== KEEP APP ALIVE =====
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
