from app.health_service import get_or_create_today_log
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

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):

    db, log = get_or_create_today_log()

    score = 0

    if log.wakeup_before_630:
        score += 15

    if log.water_ml >= 3000:
        score += 15

    if log.exercise_done:
        score += 20

    if log.steps >= 8000:
        score += 15

    if not log.alcohol:
        score += 10

    if log.breakfast_done:
        score += 10

    if log.learning_done:
        score += 5

    if log.sleep_before_11:
        score += 10

    db.close()

    await update.message.reply_text(
        f"""
📋 Baymax Daily Report

💧 Water: {int(log.water_ml)} ml
🚶 Steps: {log.steps}
🏋️ Exercise: {'✅' if log.exercise_done else '❌'}

📊 Score: {score}/100
"""
    )

async def steps(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) != 1:

        await update.message.reply_text(
            "Usage: /steps 5000"
        )

        return

    try:
        step_count = int(context.args[0])

    except ValueError:

        await update.message.reply_text(
            "Please enter a valid number."
        )

        return

    db, log = get_or_create_today_log()

    log.steps = step_count

    db.commit()

    db.close()

    await update.message.reply_text(
        f"""
🚶 Steps Updated

Current Steps:
{step_count}

Goal:
8000
"""
    )

async def exercise(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "✅ Exercise recorded."
    )

async def water(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) != 1:

        await update.message.reply_text(
            "Usage: /water 500"
        )

        return

    try:

        amount = int(context.args[0])

    except ValueError:

        await update.message.reply_text(
            "Please enter a valid number."
        )

        return

    db, log = get_or_create_today_log()

    log.water_ml += amount

    db.commit()

    total = log.water_ml

    remaining = max(0, 3000 - total)

    await update.message.reply_text(
        f"""
💧 Water Added

Added: {amount} ml

Today's Total:
{int(total)} / 3000 ml

Remaining:
{int(remaining)} ml
"""
    )

    db.close()

async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):

    db, log = get_or_create_today_log()

    score = 0

    if log.wakeup_before_630:
        score += 15

    if log.water_ml >= 3000:
        score += 15

    if log.exercise_done:
        score += 20

    if log.steps >= 8000:
        score += 15

    if not log.alcohol:
        score += 10

    if log.breakfast_done:
        score += 10

    if log.learning_done:
        score += 5

    if log.sleep_before_11:
        score += 10

    db.close()

    await update.message.reply_text(
        f"""
📊 Baymax Health Score

Today's Score:
{score}/100
"""
    )

def run_bot():

    application = (
        ApplicationBuilder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("water", water)
    )
    application.add_handler(
        CommandHandler("steps", steps)
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("ping", ping)
    )
    
    application.add_handler(
        CommandHandler("report", report)
    )

    application.add_handler(
        CommandHandler("exercise", exercise)
    )

    application.add_handler(
        CommandHandler("score", score)
    )

    print("🤖 Baymax Telegram Bot Started")

    application.run_polling()
