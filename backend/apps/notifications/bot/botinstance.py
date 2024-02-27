from telegram.ext import ApplicationBuilder
from django.conf import settings
from django.utils import translation
from mixins.enums import Locale
from apps.notifications.models import Telegram
from asgiref.sync import sync_to_async


def use_language(lang, force=False, permitted_langs: list = None):
    if permitted_langs is None:
        permitted_langs = [Locale.ru]
    if force:
        translation.activate(lang)
        return
    if lang in permitted_langs:
        translation.activate(lang)
    else:
        translation.activate('en')


async def detect_language(update, default='en'):
    try:
        language = (await sync_to_async(
            Telegram.objects.select_related('user').get)(
            chat_id=update.message.chat_id)).user.locale
    except Exception as e:
        # print("#"*20, e)
        language = default
    return language


app = ApplicationBuilder().token(settings.BOT_TOKEN).build()

# group_app = ApplicationBuilder().token(settings.GROUP_BOT_TOKEN).build()
# bot_instance = app.bot
