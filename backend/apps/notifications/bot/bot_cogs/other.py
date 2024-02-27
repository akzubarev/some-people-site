from django.utils.translation import gettext as _
from telegram.ext import ConversationHandler

from ..botinstance import use_language, detect_language
from .settings import logger


async def cancel(update, context):
    use_language(await detect_language(update))
    user = update.message.from_user
    logger.info(f"User {user.first_name} canceled the conversation.")
    update.message.reply_text(_("Bye! I hope we can talk again some day."))
    return ConversationHandler.END


def error(update, context):
    print(context.error)
    logger.warning(f'Update "{update}" caused error "{context.error}"')
