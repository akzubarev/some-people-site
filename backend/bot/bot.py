"""Telegram bot entrypoint."""
import os
import sys

import django
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

sys.path[0] = '/app/'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import bot.conversations as convo
import bot.commands as commands
import bot.jobs as jobs
import bot.other as other
import bot.const as const


def main():
    """Telegram bot entrypoint."""
    app = ApplicationBuilder().token(const.TELEGRAM_BOT_TOKEN).build()

    # Conversations
    app.add_handler(convo.login_conv_handler())

    # Commands
    app.add_handler(CommandHandler("stop", commands.stop))

    # Other Handlers
    app.add_handler(MessageHandler(filters.TEXT, other.handle_message))
    app.add_error_handler(other.error)

    # Jobs
    app.job_queue.run_repeating(jobs.notify_users, interval=60, first=0)

    app.run_polling()


if __name__ == "__main__":
    main()
