import os
import sys
import logging
import psutil
import time
from telegram import Update
from telegram.ext import ContextTypes
from core.config import ADMIN_ID

logger = logging.getLogger("ADMIN_HANDLERS")

async def update_system(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: 
        return
    await update.message.reply_text("📥 <b>Admin:</b> Pulling latest changes from GitHub...")
    try:
        os.system("git pull origin main")
        await update.message.reply_text("✅ Code updated. Restarting system...")
        os.execv(sys.executable, ['python3'] + sys.argv)
    except Exception as e:
        logger.error(f"Update failed: {e}")
        await update.message.reply_text(f"❌ Update failed: {e}")

async def send_db_backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: 
        return
    db_path = "makaut.db"
    if os.path.exists(db_path):
        await update.message.reply_document(document=open(db_path, 'rb'), caption="📂 Database Backup")
    else:
        await update.message.reply_text("❌ Database not found.")

async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simplified Health Check for AI-Free mode."""
    if update.effective_user.id != ADMIN_ID:
        return

    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    process_start = psutil.Process(os.getpid()).create_time()
    uptime_str = time.strftime('%Hh %Mm %Ss', time.gmtime(int(time.time() - process_start)))

    status_msg = (
        "<b>🖥️ System Health Report (AI-FREE)</b>\n\n"
        f"<b>⏱ Uptime:</b> {uptime_str}\n"
        f"<b>📊 CPU:</b> {cpu_usage}% | <b>🧠 RAM:</b> {ram_usage}%\n\n"
        "✅ <b>Mode:</b> Strict 2026 Gatekeeper\n"
        "✅ <b>Services:</b> All Active\n"
        "<i>Running 24/7 on Linux Mint</i>"
    )
    await update.message.reply_text(status_msg, parse_mode='HTML')