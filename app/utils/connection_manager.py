from fastapi import WebSocket, WebSocketDisconnect
from app.logger import logger
from app.utils.session import get_or_create_session
from app.crud import create_chat_message
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from contextlib import asynccontextmanager
from app.telegram_bot import send_message_to_telegram
from datetime import datetime
from app.globals import SEOUL_TIMEZONE
import json


@asynccontextmanager
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

class ConnectionManager:
    def __init__(self):
        # 사용자 ID를 키로 하는 WebSocket 연결 관리
        self.user_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        """
        WebSocket 연결을 수락하고 활성 연결 목록에 추가합니다.
        """
        await websocket.accept()
        self.user_connections[user_id] = websocket
        logger.info(f"WebSocket connection accepted: {user_id}")

    async def disconnect(self, user_id: str):
        """
        WebSocket 연결을 닫고 활성 연결 목록에서 제거합니다.
        """
        if user_id in self.user_connections:
            del self.user_connections[user_id]
            logger.info(f"WebSocket connection closed: {user_id}")

    async def send_message_to_db_and_telegram(self, user_id: str, message: dict):
        """
        WebSocket을 통해 메시지를 전송합니다.
        """
        # get_db를 직접 호출하여 세션 가져오기
        async with get_db() as db:
            # 세션 생성
            session = await get_or_create_session(user_id=user_id, db=db)

            try:
                chat_message = json.loads(message)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON message: {message}")
                return

            # 채팅 메시지 Telegram에 전송
            send_result = await send_message_to_telegram(session_id=session.id, user_id=user_id, content=json.dumps(chat_message))
            if not send_result:
                # TODO: 메세지 전송 실패 시 처리
                logger.error(f"Failed to send message to Telegram: {json.dumps(chat_message)}")
            else:
                logger.info(f"Message sent to Telegram: {json.dumps(chat_message)}")

            # 채팅 메시지 db에 생성
            chat_message = await create_chat_message(
                session_id=session.id, 
                chat_message=chat_message, 
                is_sent_to_telegram=send_result, 
                db=db
            )
            chat_message_str = json.dumps(chat_message)

            if user_id in self.user_connections:
                await self.user_connections[user_id].send_text(chat_message_str)
                logger.info(f"Message sent to {user_id}: {chat_message}")
            else:
                logger.warning(f"No active connection found for user: {user_id}")   
    
    async def send_message_to_user_telegram(self, user_id: str, message: dict):
        """
        사용자가 보낸 메세지가 db에 저장된 후 Telegram을 통해 메시지를 전송합니다.
        """
        pass

    async def send_message_from_telegram(self, telegram_message: str):
        """
        Telegram을 통해 메시지를 받아와 저장 후 WebSocket을 통해 메시지를 전송합니다.
        """
        parsed_message = telegram_message.split("\n")
        session_id = parsed_message[0].split(": ")[1]
        user_id = parsed_message[1].split(": ")[1]
        content = parsed_message[2].split(": ")[1]

        chat_message = {
            "sender_id": "jdw",
            "receiver_id": user_id,
            "content": content,
        }

        async with get_db() as db:
            chat_message = await create_chat_message(
                session_id=session_id, 
                chat_message=chat_message, 
                is_sent_to_telegram=True, 
                db=db
            )
            chat_message_str = json.dumps(chat_message)

            if user_id in self.user_connections:
                await self.user_connections[user_id].send_text(chat_message_str)
                logger.info(f"Message from Telegram sent to {user_id}: {chat_message}")
            else:
                logger.warning(f"No active connection found for user: {user_id}")

