import logging
from telegram.ext import ApplicationBuilder

from core.config import BOT_TOKEN
from bot.user_handlers import register_user_handlers

logger = logging.getLogger("TELEGRAM")

_app = None


def get_bot():
    if _app is None:
        raise RuntimeError("Telegram not initialized")
    return _app.bot


async def init_telegram():
    global _app

    logger.info("BUILDING TELEGRAM APP")

    _app = ApplicationBuilder().token(BOT_TOKEN).build()

    register_user_handlers(_app)

    logger.info("HANDLERS REGISTERED")


async def start_telegram():
    global _app

    logger.info("STARTING TELEGRAM")

    await _app.initialize()
    await _app.start()
    await _app.bot.initialize()

    # START POLLING MANUALLY (SAFE)
    await _app.updater.start_polling()

    logger.info("TELEGRAM BOT READY")
