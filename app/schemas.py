from pydantic import BaseModel


class DailyLogCreate(BaseModel):
    water_ml: float = 0
    exercise_done: bool = False
    steps: int = 0
    breakfast_done: bool = False
    alcohol: bool = False
    sleep_before_11: bool = False
    wakeup_before_630: bool = False
    learning_done: bool = False
