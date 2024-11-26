from telegram import Bot
from telegram.error import TelegramError
from app.logger import logger
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN)

async def send_telegram_message(user_id: int, content: str) -> bool:
    try:
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        content = f"User ID: {user_id}\nMessage: {content}"
        await bot.send_message(chat_id=chat_id, text=content)
        logger.info(f"Message sent from {user_id}: {content}")
        return True
    except TelegramError as e:
        logger.error(f"Failed to send message to Telegram: {e}")
        return False