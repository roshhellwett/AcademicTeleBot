import os
import sys
import asyncio
import psutil
import time
from telegram import Update
from telegram.ext import ContextTypes
from core.config import ADMIN_ID

async def update_system(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    await update.message.reply_text("📥 <b>Admin:</b> Pulling from GitHub...")
    
    process = await asyncio.create_subprocess_shell(
        "git pull origin main",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    
    if process.returncode == 0:
        await update.message.reply_text("✅ Restarting...")
        os.execv(sys.executable, ['python3'] + sys.argv)
    else:
        await update.message.reply_text(f"❌ Git Fail: {stderr.decode()}")

async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    uptime = time.strftime('%Hh %Mm', time.gmtime(time.time() - psutil.Process().create_time()))

    await update.message.reply_text(
        f"<b>🖥️ System Health (Supreme)</b>\n"
        f"Uptime: {uptime} | CPU: {cpu}% | RAM: {ram}%\n"
        f"Mode: 2026 Async Gatekeeper",
        parse_mode='HTML'
    )