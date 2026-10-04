from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from django.conf import settings

from apps.notifications.telegram_html import telegram_html

import bot.database as db
from logging import getLogger

logger = getLogger(__name__)


async def notify_users(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends new notifications to users."""
    notifications = await db.get_notifications()
    for notification in notifications:
        try:
            await context.bot.send_message(
                chat_id=notification.chat_id,
                text=telegram_html(notification.text, base_url=f'https://{settings.DOMAIN}/'),
                parse_mode=ParseMode.HTML,
            )
            await db.mark_notification_sent(notification_id=notification.id)
        except Exception as e:
            await db.mark_notification_failed(notification_id=notification.id, error_code=type(e).__name__)
            logger.warning('Notification %s delivery failed: %s', notification.id, type(e).__name__)
