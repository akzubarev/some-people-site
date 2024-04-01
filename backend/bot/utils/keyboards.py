from typing import List

from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, \
    InlineKeyboardButton

import bot.const as const


def reply_keyboard(options: List[List], placeholder: str, buttons=True):
    if buttons is True:
        keyboard = [
            [
                InlineKeyboardButton(
                    option, callback_data=str(option_id)
                )
                for option, option_id in options_sublist
            ] for options_sublist in options
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    else:
        reply_markup = ReplyKeyboardMarkup(
            options, one_time_keyboard=True,
            input_field_placeholder=placeholder
        )
    return reply_markup


def action_button(text: str, command: str, key=None):
    match command:
        case const.SIGN_UP:
            link = f"https://t.me/{const.BOT_USERNAME}"  # /?start={c.SIGN_UP}"
        # case c.SIGN_UP:
        #     link = f"t.me//{c.BOT_USERNAME}/?start={key if key is not None else ''}"
        case _:
            link = ""
    keyboard = [[InlineKeyboardButton(text, url=link)]]
    return InlineKeyboardMarkup(keyboard)
