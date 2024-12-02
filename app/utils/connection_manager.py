from fastapi import WebSocket, WebSocketDisconnect
from app.logger import logger
from app.utils.session import get_or_create_session
from app.crud import create_chat_message
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

    async def send_message_to_user(self, user_id: str, message: str):
        """
        WebSocket을 통해 메시지를 전송합니다.
        """

        # 세션 생성
        session = await get_or_create_session(user_id)

        # 채팅 메시지 생성
        chat_message = await create_chat_message(session.id, message)
        
        if user_id in self.user_connections:
            await self.user_connections[user_id].send_text(message)
            logger.info(f"Message sent to {user_id}: {message}")
        else:
            logger.warning(f"No active connection found for user: {user_id}")   
    
