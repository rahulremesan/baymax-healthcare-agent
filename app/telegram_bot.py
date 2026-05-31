from app.health_service import get_or_create_today_log

from telegram import (
    Update,
    ReplyKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from app.config import settings

user_state = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["💧 Water", "🏋️ Exercise"],
        ["🚶 Steps", "⚖️ Weight"],
        ["📊 Score", "📋 Report"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        """
🏥 Baymax Healthcare Agent

Choose an action below:
""",
        reply_markup=reply_markup
    )


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🏥 Baymax is healthy and running."
    )


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    db, log = get_or_create_today_log(user_id)

    score_value = 0

    if log.wakeup_before_630:
        score_value += 15

    if log.water_ml >= 3000:
        score_value += 15

    if log.exercise_done:
        score_value += 20

    if log.steps >= 8000:
        score_value += 15

    if not log.alcohol:
        score_value += 10

    if log.breakfast_done:
        score_value += 10

    if log.learning_done:
        score_value += 5

    if log.sleep_before_11:
        score_value += 10

    db.close()

    await update.message.reply_text(
        f"""
📋 Baymax Daily Report

💧 Water: {int(log.water_ml)} ml
🚶 Steps: {log.steps}
🏋️ Exercise: {'✅' if log.exercise_done else '❌'}

📊 Score: {score_value}/100
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

    user_id = update.effective_user.id

    db, log = get_or_create_today_log(user_id)

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

    user_id = update.effective_user.id

    db, log = get_or_create_today_log(user_id)

    log.exercise_done = True

    db.commit()

    db.close()

    await update.message.reply_text(
        """
🏋️ Exercise Recorded

Exercise Goal: ✅ Completed
"""
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

    user_id = update.effective_user.id

    db, log = get_or_create_today_log(user_id)

    log.water_ml += amount

    db.commit()

    total = log.water_ml

    remaining = max(0, 3000 - total)

    db.close()

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


async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    db, log = get_or_create_today_log(user_id)

    score_value = 0

    if log.wakeup_before_630:
        score_value += 15

    if log.water_ml >= 3000:
        score_value += 15

    if log.exercise_done:
        score_value += 20

    if log.steps >= 8000:
        score_value += 15

    if not log.alcohol:
        score_value += 10

    if log.breakfast_done:
        score_value += 10

    if log.learning_done:
        score_value += 5

    if log.sleep_before_11:
        score_value += 10

    db.close()

    await update.message.reply_text(
        f"""
📊 Baymax Health Score

Today's Score:
{score_value}/100
"""
    )


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    chat_id = update.effective_chat.id
    text = update.message.text

    if text == "💧 Water":

        user_state[chat_id] = "water"

        await update.message.reply_text(
            """
💧 Water Intake

How much water did you drink?

Examples:
500
1000
1500
"""
        )

        return

    elif text == "🚶 Steps":

        user_state[chat_id] = "steps"

        await update.message.reply_text(
            """
🚶 Steps Update

Enter your current steps.

Example:
8500
"""
        )

        return

    elif text == "🏋️ Exercise":

        await exercise(update, context)
        return

    elif text == "📊 Score":

        await score(update, context)
        return

    elif text == "📋 Report":

        await report(update, context)
        return

    elif text == "⚖️ Weight":

        await update.message.reply_text(
            "⚖️ Weight tracking coming soon."
        )

        return

    if user_state.get(chat_id) == "water":

        try:

            amount = int(text)

            user_id = update.effective_user.id
 
            db, log = get_or_create_today_log(user_id)

            log.water_ml += amount

            db.commit()

            total = log.water_ml

            remaining = max(0, 3000 - total)

            db.close()

            user_state.pop(chat_id)

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

        except ValueError:

            await update.message.reply_text(
                "Please enter a valid number."
            )

        return

    if user_state.get(chat_id) == "steps":

        try:

            step_count = int(text)

            user_id = update.effective_user.id

            db, log = get_or_create_today_log(user_id)

            log.steps = step_count

            db.commit()

            db.close()

            user_state.pop(chat_id)

            await update.message.reply_text(
                f"""
🚶 Steps Updated

Current Steps:
{step_count}

Goal:
8000
"""
            )

        except ValueError:

            await update.message.reply_text(
                "Please enter a valid number."
            )

        return


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
        CommandHandler("water", water)
    )

    application.add_handler(
        CommandHandler("steps", steps)
    )

    application.add_handler(
        CommandHandler("exercise", exercise)
    )

    application.add_handler(
        CommandHandler("score", score)
    )

    application.add_handler(
        CommandHandler("report", report)
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            button_handler
        )
    )

    print("🤖 Baymax Telegram Bot Started")

    application.run_polling()
