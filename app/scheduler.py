from apscheduler.schedulers.background import BackgroundScheduler
from app.telegram_sender import send_telegram_message

scheduler = BackgroundScheduler()


def morning_reminder():

    send_telegram_message(
        """
🌅 Good Morning Rahul

Today's Goals

□ Water 3L
□ Exercise
□ Walk 8000 Steps
□ Sleep Before 11 PM

Let's have a productive day.
"""
    )

def water_reminder():

    send_telegram_message(
        """
💧 Water Check

Target:
3000 ml

Keep drinking water.
"""
    )

def exercise_reminder():

    send_telegram_message(
        """
🏋️ Exercise Reminder

Exercise is important.

Complete today's workout before 9 PM.
"""
    )

def sleep_reminder():

    send_telegram_message(
        """
🌙 Sleep Reminder

Prepare for sleep.

Target:
Before 11 PM.
"""
    )


scheduler.add_job(
    morning_reminder,
    "cron",
    hour=6,
    minute=30
)

scheduler.add_job(
    water_reminder,
    "cron",
    hour=11,
    minute=0
)

scheduler.add_job(
    exercise_reminder,
    "cron",
    hour=19,
    minute=0
)

scheduler.add_job(
    sleep_reminder,
    "cron",
    hour=22,
    minute=0
)
scheduler.add_job(
    morning_reminder,
    "interval",
    seconds=30
)

def start_scheduler():
    scheduler.start()
    print("⏰ Baymax Scheduler Started")
