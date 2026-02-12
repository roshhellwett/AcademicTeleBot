import asyncio
import logging
import sys
import codecs
from telegram import Bot
from database.db import SessionLocal
from core.config import BOT_TOKEN, SEARCH_BOT_TOKEN, ADMIN_BOT_TOKEN

if sys.platform.startswith('win'):
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

logging.basicConfig(level=logging.INFO)

async def verify_system():
    print("\n🔍 === TELEACADEMIC AI-FREE HEALTH CHECK ===\n")

    # 1. Test Bots
    for name, token in [("MAIN", BOT_TOKEN), ("SEARCH", SEARCH_BOT_TOKEN), ("ADMIN", ADMIN_BOT_TOKEN)]:
        try:
            bot = Bot(token=token)
            me = await bot.get_me()
            print(f"✅ {name} BOT: @{me.username} is Online")
        except Exception as e:
            print(f"❌ {name} BOT: Failed | {e}")

    # 2. Test Database
    try:
        db = SessionLocal()
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        print("✅ DATABASE: Connection Successful")
        db.close()
    except Exception as e:
        print(f"❌ DATABASE: Failed | {e}")

    print("\n🚀 === CHECK COMPLETE ===\n")

if __name__ == "__main__":
    asyncio.run(verify_system())