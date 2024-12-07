from telegram.ext import ApplicationBuilder, Application
from telegram.error import TelegramError
from app.logger import logger
import os
import json

# 환경 변수에서 토큰과 채널 ID 가져오기
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Application 객체 생성 (봇 설정)
application: Application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

async def send_message_to_telegram(session_id: int, user_id: int, content: str) -> bool:
    try:
        message = json.loads(content).get("content")
        # 메세지 내용 구성
        message_content = f"Session ID: {session_id}\nUser ID: {user_id}\nContent: {message}"

        # Application 객체의 bot을 사용해 메세지 전송
        await application.bot.send_message(chat_id=int(TELEGRAM_CHAT_ID), text=message_content)

        # 성공 로그 기록
        logger.info(f"Message sent from {user_id}: {message_content}")
        return True
    except TelegramError as e:
        # 실패 로그 기록
        logger.error(f"Failed to send message to Telegram: {e}")
        return False
