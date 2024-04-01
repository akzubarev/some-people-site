import asyncio
import os
import sys
import traceback
from time import sleep

import logging
import django
from asgiref.sync import sync_to_async

sys.path[0] += '/../../..'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.notifications.models import Telegram
from apps.notifications.models import Notification
from apps.notifications.bot.botinstance import app
from apps.notifications.daemons.utils.send_image import send_image

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


async def send_first(bot):
    while True:
        notifications = Notification.objects.filter(
            telegram=Notification.Status.NEW
        ).select_related('user', 'user__telegram').exclude(
            key='TelegramBotNotification').exclude(user_id=1)
        async for notif in notifications:
            try:
                if (chat := notif.user.telegram.chat_id) is not None:
                    await send_image(notif, bot, chat)
                else:
                    notif.telegram = notif.Status.CANCELLED
                    await sync_to_async(notif.save)()

            except Telegram.DoesNotExist:
                notif.telegram = notif.Status.CANCELLED
                await sync_to_async(notif.save)()

            except Exception as e:
                # if 'not exist' in str(e):
                notif.telegram = notif.Status.CANCELLED
                await sync_to_async(notif.save)()
                logger.error(traceback.format_exc())
                logger.error(notif.id)
                logger.error(e)
            sleep(.3)
        sleep(5)


if __name__ == '__main__':
    asyncio.run(send_first(bot=app.bot))
