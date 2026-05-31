from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from app.config import settings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = """
🤖 Baymax Healthcare Agent

Available Commands

/start
/exercise
/score
/ping

Baymax is online.
"""

    await update.message.reply_text(message)


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🏥 Baymax is healthy and running."
    )


async def exercise(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "✅ Exercise recorded."
    )


async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📊 Score feature coming soon."
    )


def run_bot():

    application = (
        ApplicationBuilder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("ping", ping)
    )

    application.add_handler(
        CommandHandler("exercise", exercise)
    )

    application.add_handler(
        CommandHandler("score", score)
    )

    print("🤖 Baymax Telegram Bot Started")

    application.run_polling()
