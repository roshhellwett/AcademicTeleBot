import asyncio
import logging

from database.db import SessionLocal
from database.models import Subscriber
from bot.telegram_app import get_bot

logger = logging.getLogger("BROADCASTER")


async def broadcast(notifications):

    bot = get_bot()

    db = SessionLocal()

    subs = db.query(Subscriber).filter_by(active=True).all()

    if not subs:
        logger.warning("NO SUBSCRIBERS FOUND")
        db.close()
        return

    success = 0
    failed = 0

    for n in notifications:

        message = (
            "🎓 MAKAUT NEW NOTIFICATION\n\n"
            f"📌 {n['title']}\n\n"
            f"🏛 Source: {n['source']}\n"
            f"🔗 {n['source_url']}\n\n"
            "━━━━━━━━━━━━━━\n"
            "TeleAcademic Bot"
        )

        for sub in subs:
            try:
                await bot.send_message(
                    chat_id=sub.telegram_id,
                    text=message,
                    disable_web_page_preview=True
                )

                success += 1
                await asyncio.sleep(0.05)

            except Exception as e:
                failed += 1
                logger.error(f"FAIL {sub.telegram_id} {e}")

    db.close()

    logger.info(f"BROADCAST DONE success={success} failed={failed}")
