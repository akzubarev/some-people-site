import pycld2 as cld2

from django.utils.translation import get_language
from ..botinstance import use_language, detect_language
from ...utils.telegram_utils import \
    get_reply_keyboard, get_keyboard_conf


async def handle_keyboard(update, context):
    try:
        if update.message.chat_id < 0:
            return
    except AttributeError:
        return

    use_language(await detect_language(update), force=True)

    for kb in get_keyboard_conf().values():
        if kb["message"] == update.message.text:
            context = {
                "lang": get_language(),
            }
            # mg = f"https://residual.community/docs/presentation-{context['lang']}.pdf"
            # print("*" *20, mg)
            # await update.message.reply_document(open(f"../frontend/public/docs/presentation-{context['lang']}.pdf", "rb"))
            await update.message.delete()
            for handler in kb["handlers"]:
                await getattr(update.message, handler["method"])(**{
                    "reply_markup": get_reply_keyboard(),
                    **handler["kwargs"](context)
                })
            return
    await update.message.reply_text(
        "Excuse me, but I do not understand... Try again",
        reply_markup=get_reply_keyboard())


def check_spam(update, context):
    _, _, langs = cld2.detect(update.message.text)

    for lang in langs:
        if lang[1] in ['hi', 'ar', 'fa', 'uz']:
            update.message.delete()
            return
