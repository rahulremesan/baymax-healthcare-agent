import requests

from app.config import settings


def send_telegram_message(message):

    url = (
        f"https://api.telegram.org/bot"
        f"{settings.TELEGRAM_BOT_TOKEN}"
        f"/sendMessage"
    )

    requests.post(
        url,
        json={
            "chat_id": settings.CHAT_ID,
            "text": message
        }
    )
