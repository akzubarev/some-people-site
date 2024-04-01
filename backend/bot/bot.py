import os
import sys

import django
from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder
from telegram.ext import filters

sys.path[0] += "/../../.."
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from config import settings
import bot.conversations as convo
import bot.commands as commands
import bot.other as other

def main():
    app = ApplicationBuilder().token(settings.BOT_TOKEN).build()

    app.add_handler(convo.login_conv_handler())
    app.add_handler(CommandHandler("stop", commands.stop))

    app.add_handler(MessageHandler(filters.TEXT, other.handle_message))
    app.add_error_handler(other.error)

    app.run_polling()


if __name__ == "__main__":
    main()
