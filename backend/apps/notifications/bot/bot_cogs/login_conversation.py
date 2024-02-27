from asgiref.sync import sync_to_async
from django.utils.translation import gettext as _
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler
from telegram.ext import filters

from ..botinstance import app, use_language, \
    detect_language
from ...models import Telegram
from ...utils.telegram_utils import \
    generate_telegram_code, get_reply_keyboard
from apps.users.models import User
from apps.users.utils import decode_uid
from .commands import stop
from .settings import DOMAIN

EV, CODE, PROMO = range(3)


async def start(update, context):
    use_language(await detect_language(update))

    mes = update.message
    telega = mes.chat_id

    if telega < 0:
        await update.message.delete()
        return ConversationHandler.END

    if context.args:
        return await code(update, context)
    else:
        await update.message.reply_text(
            text=(
                _('Hello! Please enter your personal code from the page. <a href="{url}">Go back to website</a>').format(
                    url=DOMAIN)
            ), parse_mode=ParseMode.HTML)
        return CODE


async def code(update, context):
    use_language(await detect_language(update))

    mes = update.message
    telega = mes.chat_id
    username = mes['chat']['username']
    first_name = mes['chat']['first_name']
    if telega < 0:
        update.message.delete()
        return ConversationHandler.END

    code = context.args[0] if context.args else mes.text
    user_id = decode_uid(code[32:])
    shifr = generate_telegram_code(user_id)

    if shifr[:32] == code[:32]:
        try:
            user = await sync_to_async(User.objects.get)(id=int(user_id))
            user_has_tg = await sync_to_async(
                Telegram.objects.filter(chat_id=telega).exclude(
                    user_id=user_id).exists)()
            if user_has_tg:
                await mes.reply_text(
                    text=_('This telegram is already in use, connect another'))
                return CODE
            queryset = Telegram.objects.filter(user=user)
            if await sync_to_async(queryset.count)():
                chat_id = (await sync_to_async(list)(queryset))[0].chat_id
                if chat_id:
                    if str(chat_id) != str(telega):
                        await sync_to_async(
                            Telegram(
                                id=queryset[0].id,
                                user=user, username=username, code=code,
                                first_name=first_name, chat_id=telega,
                            ).save)()
                        await mes.reply_text(
                            text=_('Telegram account updated'))
                        return ConversationHandler.END
                    else:
                        await mes.reply_text(text=_(
                            'Telegram is already connected to your account'))
                        return ConversationHandler.END
                await sync_to_async(queryset.update)(
                    username=username, first_name=first_name,
                    chat_id=telega
                )
            else:
                await sync_to_async(Telegram(
                    user=user, username=username,
                    first_name=first_name, chat_id=telega, code=code
                ).save)()
            if not user.avatar:
                from django.core.files import File
                from urllib.request import urlretrieve
                photos = (await app.bot.getUserProfilePhotos(telega))['photos']
                if len(photos):
                    url = (await app.bot.getFile(photos[0][-1]['file_id']))[
                        'file_path']
                    await sync_to_async(user.avatar.save)('image.png', File(
                        open(urlretrieve(url)[0], 'rb')))
        except User.DoesNotExist:
            await mes.reply_text(text=_("Invalid code, try again, please"))
            return CODE
    else:
        await mes.reply_text(text=_("Invalid code, try again, please"))
        return CODE

    await mes.reply_text(text=_(
        'Your Telegram has been verified, '
        'now I can send you important notifications. '
        '<a href="{url}">Go back to website</a>').format(
        url=DOMAIN), parse_mode=ParseMode.HTML,
        reply_markup=get_reply_keyboard())
    return ConversationHandler.END


def login_conv_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={CODE: [MessageHandler(filters.TEXT, code)], },
        allow_reentry=True,
        fallbacks=[CommandHandler("stop", stop)],
    )
