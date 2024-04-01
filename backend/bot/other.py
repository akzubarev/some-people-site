import logging

from telegram import Update
from telegram.ext import ContextTypes
import apps.notifications.bot.const as const
import apps.notifications.bot.responses as resp

logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    logger.info(f"{update.message.chat.id}")
    if message_type in ["group", "supergroup"]:
        if f"@{c.BOT_USERNAME}" in text:
            new_text = text.replace(f"@{const.BOT_USERNAME}", '').strip()
            await update.message.reply_text(resp.handle_response(text=new_text))
    else:
        await update.message.reply_text(resp.handle_response(text=text))


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Update {update} caused error: {context.error}")
