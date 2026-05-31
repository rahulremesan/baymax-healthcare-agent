from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy import BigInteger

from app.database import Base


class DailyLog(Base):
    __tablename__ = "daily_logs"

    id = Column(Integer, primary_key=True, index=True)

    telegram_user_id = Column(
        BigInteger,
        index=True
    )

    date = Column(String)

    water_ml = Column(Float, default=0)

    exercise_done = Column(Boolean, default=False)

    steps = Column(Integer, default=0)

    breakfast_done = Column(Boolean, default=False)

    alcohol = Column(Boolean, default=False)

    sleep_before_11 = Column(Boolean, default=False)

    wakeup_before_630 = Column(Boolean, default=False)

    learning_done = Column(Boolean, default=False)
