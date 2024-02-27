import logging
from time import sleep

import telegram
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup as BSHTML
from html_sanitizer import Sanitizer

from utils.list_handling import batched
from .telegram_catch import telegram_exception_catcher
from apps.notifications.bot.botinstance import use_language

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


@telegram_exception_catcher
async def send_image(notif, bot, chat):
    withCaption = True
    if isinstance(chat, dict):
        use_language(chat["language"])
        chat = chat["id"]
        withCaption = False
    else:
        use_language(await sync_to_async(lambda: notif.user.locale)())
    # reply_markup=reply_markup,
    image = await sync_to_async(lambda: notif.type.get('image', False))()
    title = await sync_to_async(lambda: notif.type.get('title', ''))()
    message = await sync_to_async(lambda: notif.type.get('description', ''))()
    logger.debug(image)
    if image:
        await bot.send_photo(
            chat, image,
            caption=f"{title}\n\n{message}" if withCaption else None,
            parse_mode=telegram.constants.ParseMode.HTML
        )
    else:
        await bot.send_message(
            chat, title + message, parse_mode=telegram.constants.ParseMode.HTML
        )

    notif.telegram = notif.Status.SUCCESS
    await sync_to_async(notif.save)()

    sleep(1)


@telegram_exception_catcher
async def send_media_groups(notif, bot, chat):
    images = []
    if notif.mailing.image:
        images.append(notif.mailing.image.url)

    soup = BSHTML(notif.mailing.text, features="lxml")
    for image in soup.findAll('img'):
        images.append(image['src'])

    message = Sanitizer({
        "tags": {'a', 'br', 'b', 'strong', 'i', 'em', 'code',
                 's', 'strike', 'del', 'u'},
        # "attributes": {}, "whitespace": {},
        'empty': {'a', 'br'}, 'separate': {'br'},
    }).sanitize(notif.mailing.text.replace("\n", "<br>"))
    # sanitizer lib is fucked up
    message = message.replace("<br>", "\n")

    if len(images) < 1:
        await bot.send_message(
            chat, message, parse_mode=telegram.constants.ParseMode.HTML
        )
    else:
        for i, media_group in enumerate(batched(images, batch_size=10)):
            await bot.send_media_group(
                chat, [
                    telegram.InputMediaPhoto(f"https://residual.community{p}")
                    for p in media_group
                ],
                caption=message if i == 0 else None,
                parse_mode=telegram.constants.ParseMode.HTML
            )
            sleep(0.15)

    notif.telegram = notif.Status.SUCCESS
    await sync_to_async(notif.save)()
