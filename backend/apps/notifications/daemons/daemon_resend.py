import os
import sys
import logging
from time import sleep

import django
from django.db.models import Q
from django.forms import model_to_dict

sys.path[0] += '/../../..'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.notifications.models import Notification
from apps.notifications.bot.botinstance import app

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def resend(bot):
    while True:
        notifications = Notification.objects.filter(
            Q(telegram=Notification.Status.TIMEOUT) | Q(
                telegram=Notification.Status.NETWORK_ERROR) | Q(
                telegram=Notification.Status.TELEGRAM_CONFL))
        for notif in notifications:
            if (chat := notif.user.telegram.chat_id) is not None:
                message = f"{notif.type.get('title', '')}\n{notif.type.get('description', '')}"
                bot.send_message(model_to_dict(notif), chat, message)
            else:
                notif.telegram = notif.Status.CANCELLED
                notif.save()
        sleep(10)


if __name__ == '__main__':
    resend(bot=app.bot)
