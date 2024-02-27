from hashlib import md5

from backend import settings
from apps.users.utils import encode_uid
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from django.utils.translation import gettext as _
from backend.settings import DOMAIN


def get_with_lang(dct, lang, default_lang="en"):
    return dct[lang if lang in dct else default_lang]

def get_keyboard_conf():
    return {
        "site": {
            "message": u'\U0001F30F ' + _("Site"),
            "handlers": [{
                "method": "reply_text",
                "kwargs": lambda ctx: {
                    "text": f"[🌐](https://{DOMAIN})",
                    "parse_mode": "markdown",
                    "reply_markup": InlineKeyboardMarkup([[InlineKeyboardButton(_("Open site"), url=f"https://{DOMAIN}/")]])
                }
            }]
        },
    }


def generate_telegram_code(user_id):
    uid = encode_uid(int(user_id))
    shifr = md5(str(user_id).encode() + settings.SECRET_KEY.encode()).hexdigest()
    code = "{}{}".format(shifr, uid)
    return code

def get_reply_keyboard():
    KEYBOARD = get_keyboard_conf()
    return ReplyKeyboardMarkup([
        [KEYBOARD["site"]["message"]]
    ], resize_keyboard=True)
