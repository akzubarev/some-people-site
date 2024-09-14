"""Bot miscelanious functions."""
import logging

from telegram import Update
from telegram.ext import ContextTypes

import bot.const as const
import bot.responses as resp

logger = logging.getLogger(__name__)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles messages that are not handled by other functions."""
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    logger.info(f"{update.message.chat.id}")
    if message_type in ["group", "supergroup"]:
        if f"@{const.TELEGRAM_BOT_USERNAME}" in text:
            new_text = text.replace(f"@{const.TELEGRAM_BOT_USERNAME}", '').strip()
            await update.message.reply_text(resp.handle_response(text=new_text))
    else:
        await update.message.reply_text(resp.handle_response(text=text))


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles errors."""
    logger.info(f"Update {update} caused error: {context.error}")
