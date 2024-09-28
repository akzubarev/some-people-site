from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import bot.database as db
from logging import getLogger

logger = getLogger(__name__)


async def notify_users(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends new notifications to users."""
    notifications = await db.get_notifications()
    for notification in notifications:
        try:
            await context.bot.send_message(
                chat_id=notification.chat_id, text=notification.text,
                parse_mode=ParseMode.HTML,
            )
            await db.mark_notification_sent(notification_id=notification.id)
        except Exception as e:
            logger.exception(e)
