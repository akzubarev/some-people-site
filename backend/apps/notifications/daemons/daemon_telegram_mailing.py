import asyncio
import logging
import os
import sys
import traceback
from time import sleep

import django
from asgiref.sync import sync_to_async

sys.path[0] += '/../../..'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.notifications.bot.botinstance import app
from apps.notifications.models import MailingRecipient
from apps.notifications.models import Telegram
from apps.notifications.daemons.utils.send_image import send_media_groups

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


async def send_mailing(bot):
    while True:
        notifications = MailingRecipient.objects.select_related(
            'user', 'user__telegram', 'mailing'
        ).filter(telegram=MailingRecipient.Status.NEW, mailing__telegram=True)
        async for notif in notifications:
            try:
                user = notif.user
                chat = user.telegram.chat_id
                if chat is not None:
                    await send_media_groups(notif, bot, chat)
                else:
                    notif.telegram = notif.Status.CANCELLED
                    await sync_to_async(notif.save)()

            except Telegram.DoesNotExist:
                notif.telegram = notif.Status.CANCELLED
                await sync_to_async(notif.save)()

            except Exception as e:
                logger.error(traceback.format_exc())
            # sleep(0.05)
            sleep(5)
        sleep(5)


if __name__ == '__main__':
    asyncio.run(send_mailing(bot=app.bot))
