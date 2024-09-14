"""Database functions for notifications app."""
from datetime import datetime
from typing import List

from asgiref.sync import sync_to_async
from django.utils.timezone import make_aware

from apps.notifications.models import Notification
from apps.notifications.models.notification import NotificationData


@sync_to_async()
def mark_notifications_read(user_chat_id: str) -> None:
    """Mark all users notifications as read."""
    notifications = Notification.objects.filter(chat_id=user_chat_id)
    for notification in notifications:
        notification.viewed = True
    Notification.objects.bulk_update(notifications)


@sync_to_async()
def mark_notification_sent(notification_id: str) -> None:
    """Mark notification as sent."""
    notification = Notification.objects.filter(id=notification_id).first()
    if not notification:
        raise ValueError(f'Notification with id {notification_id} does not exist.')
    notification.sent = True
    notification.save()


@sync_to_async()
def get_notifications(chat_id: str | None = None) -> List[NotificationData]:
    """Gets all notifications for a given chat_id or all notifications."""
    notifications = Notification.objects.filter(sent=False)
    notifications = notifications.select_related('mailing').filter(
        mailing__time__lte=make_aware(datetime.now()),
        user__telegram_chat_id__isnull=False,
    )
    if chat_id:
        notifications = notifications.prefetch_related('user').filter(user__telegram_chat_id=chat_id)
    return [notification.data() for notification in notifications]
