from datetime import date

from app.database import SessionLocal
from app.database import Base
from app.database import engine

from app.models import DailyLog

Base.metadata.create_all(bind=engine)


def get_or_create_today_log(user_id):

    db = SessionLocal()

    today = str(date.today())

    log = (
        db.query(DailyLog)
        .filter(
            DailyLog.date == today,
            DailyLog.telegram_user_id == user_id
        )
        .first()
    )

    if not log:

        log = DailyLog(
            date=today,
            telegram_user_id=user_id
        )

        db.add(log)
        db.commit()
        db.refresh(log)

    return db, log
