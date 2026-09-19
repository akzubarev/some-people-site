"""Login conversation."""
from telegram import ReplyKeyboardRemove, Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from collections import deque
from functools import lru_cache
from time import monotonic

import bot.database as db

CODE = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.effective_chat or update.effective_chat.type != 'private':
        return ConversationHandler.END
    if not context.args:
        await update.message.reply_text(
            text='Привет, бот не смог достать код из ссылки, по которой ты перешел. Введи, пожалуйста, код с сайта',
            parse_mode=ParseMode.HTML
        )
        return CODE
    return await code(update=update, context=context)


async def code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Checks the equality of specified code to the user code."""
    if not update.effective_chat or update.effective_chat.type != 'private':
        return ConversationHandler.END
    attempts = chat_attempts(update.effective_chat.id)
    now = monotonic()
    while attempts and attempts[0] <= now - 60:
        attempts.popleft()
    if len(attempts) >= 5:
        await update.message.reply_text('Слишком много попыток. Подождите минуту.')
        return CODE
    attempts.append(now)
    auth_code = context.args[0] if context.args else update.message.text.strip()
    try:
        change = await db.user_tg(
            code=auth_code, chat_id=update.effective_chat.id,
            username=update.effective_user.username,
        )
    except ValueError:
        await update.message.reply_text('Неверный или просроченный код. Получите новый код на сайте.')
        return CODE
    reply_text = 'Телеграм успешно изменен.' if change else 'Телеграм успешно добавлен.'
    await update.message.reply_text(text=reply_text, reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


@lru_cache(maxsize=10000)
def chat_attempts(chat_id):
    """Bounded, per-process abuse guard; token validation remains authoritative."""
    return deque()


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels the conversation."""
    await update.message.reply_text(
        text='Регистрация отменена',
        reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.HTML,
    )
    return ConversationHandler.END


def login_conv_handler():
    """Login conversation handler."""
    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={CODE: [MessageHandler(filters.TEXT, code)], },
        allow_reentry=True,
        fallbacks=[CommandHandler("cancel", cancel)],
    )
