"""Login conversation."""
from telegram import ReplyKeyboardRemove, Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

import bot.database as db
from bot.utils.auth import not_group
from logging import getLogger

from utils.auth import decode_uuid

logger = getLogger(__name__)

CODE = 0


@not_group
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not context.args:
        await update.message.reply_text(
            text='Привет, бот не смог достать код из ссылки, по которой ты перешел. Введи, пожалуйста, код с сайта',
            parse_mode=ParseMode.HTML
        )
        return CODE
    return await code(update=update, context=context)


async def code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Checks the equality of specified code to the user code."""
    auth_code = context.args[0] if context.args else update.message.text.strip()
    # try:
    logger.warning(auth_code)
    user_uuid = decode_uuid(encoded=auth_code)
    logger.warning(user_uuid)
    change = await db.user_tg(
        user_uuid=user_uuid, chat_id=update.message.chat_id,
        username=update.message.from_user.username,
    )
    reply_text = 'Телеграм успешно изменен.' if change else 'Телеграм успешно добавлен.'
    await update.message.reply_text(text=reply_text, reply_markup=ReplyKeyboardRemove())
    # except Exception as e:
    #     await update.message.reply_text(text='Неверный код, попробуйте еще раз.')
    #     return CODE

    return ConversationHandler.END


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
