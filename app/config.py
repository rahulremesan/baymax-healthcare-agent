from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")


settings = Settings()
