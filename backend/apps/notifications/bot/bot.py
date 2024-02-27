import os
import sys

import django

from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import filters

sys.path[0] += "/../../.."
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from apps.notifications.bot.botinstance import app
from apps.notifications.bot.bot_cogs import commands as bot_commands, \
    messages as bot_messages, login_conv_handler, utils as bot_utils, \
    error as error_handler


def main():
    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS, bot_messages.new_member
        )
    )
    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.LEFT_CHAT_MEMBER, bot_messages.left_member
        )
    )

    app.add_handler(login_conv_handler())
    app.add_handler(CommandHandler("email", bot_commands.print_email))
    app.add_handler(CommandHandler("stop", bot_commands.stop))

    # app.add_handler(MessageHandler(filters.TEXT, bot_utils.check_spam))
    app.add_handler(MessageHandler(filters.TEXT, bot_utils.handle_keyboard))

    app.add_error_handler(error_handler)

    app.run_polling()


if __name__ == "__main__":
    main()
