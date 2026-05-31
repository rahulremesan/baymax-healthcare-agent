from datetime import date

from app.database import SessionLocal
from app.models import DailyLog


def get_or_create_today_log():

    db = SessionLocal()

    today = str(date.today())

    log = (
        db.query(DailyLog)
        .filter(DailyLog.date == today)
        .first()
    )

    if not log:

        log = DailyLog(
            date=today
        )

        db.add(log)
        db.commit()
        db.refresh(log)

    return db, log
