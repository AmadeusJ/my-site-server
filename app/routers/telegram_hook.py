from fastapi import APIRouter, Request
from telegram.ext import ApplicationBuilder, Application
from telegram import Update
from app.routers.websocket import manager   # 연결된 웹소켓 관리자
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_PATH = "/webhook"

router = APIRouter()


# ApplicationBuilder로 봇 앱 생성 (이제 Bot 대신 Application 사용)
application: Application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

@router.post(WEBHOOK_PATH)
async def handle_webhook(request: Request):
    try:
        # 요청으로부터 Telegram 업데이트 데이터 파싱
        json_data = await request.json()
        update = Update.de_json(json_data, bot=application.bot)

        # 사용자의 메시지 가져오기
        if update.message:
            user_message = update.message.text
            user_id = update.message.chat.id

            # 로그 출력 (로거 사용 가능)
            print(f"Received message from {user_id}: {user_message}")
            await manager.send_message_from_telegram(telegram_message=user_message)

            # 봇이 사용자에게 답장 보내기
            response_message = f"[Hook Log]\nYou said: {user_message}\n[\Hook Log]"
            await application.bot.send_message(chat_id=user_id, text=response_message)

        return {"status": "ok"}
    except Exception as e:
        print(f"Error handling webhook: {e}")
        return {"status": "error", "message": str(e)}