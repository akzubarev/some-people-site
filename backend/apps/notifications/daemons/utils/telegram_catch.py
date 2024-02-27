from asgiref.sync import sync_to_async
import logging
from telegram.error import ChatMigrated, RetryAfter, TimedOut, NetworkError, \
    BadRequest, Conflict, InvalidToken

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def telegram_exception_catcher(func):
    async def wrapped(notif, bot, chat, *args, **kwargs):
        try:
            await func(notif, bot, chat, *args, **kwargs)
        except RetryAfter as RA:
            logger.warning(f'Telegram flood exceeded - "{RA.message}"')
            await bot.send_message(chat, RA.message, timeout=RA.retry_after)

        except ChatMigrated as e:
            new_id = e.new_chat_id
            notif.user.telegram.chat_id = new_id
            await sync_to_async(notif.user.telegram.save)()

        except TimedOut as TO:
            logger.warning(
                f'Telegram to user "{notif.user_id}" TimedOut - "{TO.message}"'
            )
            notif.telegram = notif.Status.TIMEOUT
            await sync_to_async(notif.save)()

        except BadRequest as e:
            logger.warning(
                f'BadRequest at sending message "{e.message}" to user '
                f'"{notif.user_id}" with chat id "{chat}"',
            )
            notif.telegram = notif.Status.BAD_REQUEST
            await sync_to_async(notif.save)()

        except NetworkError as n:
            logger.warning(n)
            logger.warning(
                f'NetworkError at sending message to user '
                f'"{notif.user_id}" with chat id "{chat}"'
            )
            notif.telegram = notif.Status.NETWORK_ERROR
            await sync_to_async(notif.save)()

        except Conflict as cnflct:
            logger.warning(f'Telegram server conflict - "{cnflct.message}"')
            notif.telegram = notif.Status.TELEGRAM_CONFL
            await sync_to_async(notif.save)()

        except InvalidToken:
            logger.error('IMMEDIATELY CHANGE TELEGRAM TOKEN!!!')
            notif.telegram = notif.Status.TOKEN_ERROR
            await sync_to_async(notif.save)()

        # except Unauthorized:
        #     logger.warning('User with id "%s" deleted bot', notif.user_id)
        #     notif.user.telegram.chat_id = None
        #     notif.user.telegram.save()
        #     notif.telegram = notif.Status.CANCELLED
        #     notif.save()
        #     Notification(
        #     user=notif.user, key='TelegramBotNotification',
        #     data=TelegramBotNotification(bot_username='@in_game_bot').__dict__
        #     ).save()

    return wrapped
