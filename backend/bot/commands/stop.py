from asgiref.sync import sync_to_async
from django.utils.translation import gettext as _


async def stop(update, context):
    if update.message.chat_id > 0:
        tg = Telegram.objects.filter(chat_id=update.message.chat_id)
        if await sync_to_async(tg.exists)():
            await sync_to_async(tg.delete)()
            await update.message.reply_text(
                _('Telegram is disconnected from the account on the site.'))
        else:
            await update.message.reply_text(
                _('This telegram account is not connected to any account on the site.'))
