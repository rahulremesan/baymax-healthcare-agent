from datetime import date

from fastapi import FastAPI
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import Base
from app.database import engine
from app.database import get_db

from app.models import DailyLog
from app.schemas import DailyLogCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Baymax Healthcare Agent",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "status": "healthy",
        "service": "baymax"
    }


@app.post("/daily-log")
def create_daily_log(
    payload: DailyLogCreate,
    db: Session = Depends(get_db)
):

    today = str(date.today())

    existing_log = (
        db.query(DailyLog)
        .filter(DailyLog.date == today)
        .first()
    )

    if existing_log:

        existing_log.water_ml = payload.water_ml
        existing_log.exercise_done = payload.exercise_done
        existing_log.steps = payload.steps
        existing_log.breakfast_done = payload.breakfast_done
        existing_log.alcohol = payload.alcohol
        existing_log.sleep_before_11 = payload.sleep_before_11
        existing_log.wakeup_before_630 = payload.wakeup_before_630
        existing_log.learning_done = payload.learning_done

        db.commit()

        return {
            "message": "Today's log updated"
        }

    log = DailyLog(
        date=today,
        water_ml=payload.water_ml,
        exercise_done=payload.exercise_done,
        steps=payload.steps,
        breakfast_done=payload.breakfast_done,
        alcohol=payload.alcohol,
        sleep_before_11=payload.sleep_before_11,
        wakeup_before_630=payload.wakeup_before_630,
        learning_done=payload.learning_done
    )

    db.add(log)
    db.commit()

    return {
        "message": "Today's log created"
    }


@app.get("/today")
def get_today(db: Session = Depends(get_db)):

    today = str(date.today())

    log = (
        db.query(DailyLog)
        .filter(DailyLog.date == today)
        .first()
    )

    if not log:
        return {
            "message": "No log found"
        }

    return {
        "date": log.date,
        "water_ml": log.water_ml,
        "exercise_done": log.exercise_done,
        "steps": log.steps,
        "breakfast_done": log.breakfast_done,
        "alcohol": log.alcohol,
        "sleep_before_11": log.sleep_before_11,
        "wakeup_before_630": log.wakeup_before_630,
        "learning_done": log.learning_done
    }


@app.get("/health-score")
def health_score(db: Session = Depends(get_db)):

    today = str(date.today())

    log = (
        db.query(DailyLog)
        .filter(DailyLog.date == today)
        .first()
    )

    if not log:
        return {
            "score": 0,
            "message": "No data found"
        }

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

    return {
        "date": today,
        "score": score
    }


@app.get("/report")
def report(db: Session = Depends(get_db)):

    today = str(date.today())

    log = (
        db.query(DailyLog)
        .filter(DailyLog.date == today)
        .first()
    )

    if not log:
        return {
            "message": "No data found"
        }

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

    return {
        "date": today,
        "score": score,
        "water_ml": log.water_ml,
        "steps": log.steps,
        "exercise_done": log.exercise_done,
        "breakfast_done": log.breakfast_done,
        "sleep_before_11": log.sleep_before_11,
        "wakeup_before_630": log.wakeup_before_630,
        "learning_done": log.learning_done,
        "alcohol": log.alcohol
    }
