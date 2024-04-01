from urllib.request import urlretrieve

from django.core.files import File
from django.utils.translation import gettext as _
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import filters
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, \
    ContextTypes

import bot.database as db
from bot.utils.auth import not_group, decode_uid, generate_telegram_code

EV, CODE, PROMO = range(3)


@not_group
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        return await code(update, context)
    else:
        await update.message.reply_text(
            text="Привет, я не смог достать код из ссылки, по которой ты перешел. Введи, пожалуйста, код с сайта",
            parse_mode=ParseMode.HTML
        )
        return CODE


async def code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user = message.from_user

    auth_code = context.args[0] if context.args else message.text.strip()
    user_id = decode_uid(auth_code[32:])
    encoded = generate_telegram_code(user_id)

    if encoded[:32] != auth_code[:32]:
        await message.reply_text(text=_("Invalid code, try again, please"))
        return CODE
    try:
        success, message = await db.user_tg(
            user_id=user_id, chat_id=message.chat_id
        )
        if not success:
            await message.reply_text(text=message)
            return CODE

        photos = await user.get_profile_photos()
        if len(photos.photos) > 0:
            avatar_uri = photos.photos[0][-1]['file_id']
            url = await context.bot.getFile(avatar_uri)
            with open(urlretrieve(url['file_path'])[0], 'rb') as ph:
                await db.user_avatar(user_id=user_id, photo=File(ph))

    except Exception as e:
        await message.reply_text(text="Неверный код, попробуйте еще раp")
        return CODE

    await message.reply_text(
        text='Телеграм успешно добавлен', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        f"регистрация отменена",
        reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.HTML,
    )
    return ConversationHandler.END


def login_conv_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={CODE: [MessageHandler(filters.TEXT, code)], },
        allow_reentry=True,
        fallbacks=[CommandHandler("cancel", cancel)],
    )
