from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from database.db import SessionLocal
from database.models import Subscriber


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_user.id)

    db = SessionLocal()

    sub = db.query(Subscriber).filter_by(telegram_id=user_id).first()

    if not sub:
        sub = Subscriber(telegram_id=user_id, active=True)
        db.add(sub)
        db.commit()

    db.close()

    await update.message.reply_text(
        "✅ You are subscribed to MAKAUT notifications."
    )


def register_user_handlers(app):
    app.add_handler(CommandHandler("start", start_cmd))
