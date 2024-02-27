from asgiref.sync import sync_to_async
from django.utils.translation import gettext as _

from ..botinstance import use_language, detect_language
from ...models import Telegram


async def print_email(update, context):
    use_language(await detect_language(update))

    if update.message.chat_id > 0:
        tg = Telegram.objects.filter(
            chat_id=update.message.chat_id).select_related('user')
        if await sync_to_async(tg.exists)():
            await update.message.reply_text(_('Your email:') + ' ' + str(
                (await sync_to_async(tg.first)()).user.email))
        else:
            await update.message.reply_text(
                _('This telegram account is not connected to any account on the site.'))


async def stop(update, context):
    use_language(await detect_language(update))
    if update.message.chat_id > 0:
        tg = Telegram.objects.filter(chat_id=update.message.chat_id)
        if await sync_to_async(tg.exists)():
            await sync_to_async(tg.delete)()
            await update.message.reply_text(
                _('Telegram is disconnected from the account on the site.'))
        else:
            await update.message.reply_text(
                _('This telegram account is not connected to any account on the site.'))
