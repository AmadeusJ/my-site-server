from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.utils.connection_manager import ConnectionManager
from app.logger import logger

router = APIRouter()

# 웹소켓 연결 관리자 인스턴스 생성
manager = ConnectionManager()



@router.websocket("/messages")
async def websocket_endpoint(websocket: WebSocket, user_id: str = Query('default_user_id')):
    """
    WebSocket Endpoint for real-time communication.
    """
    print(f"Received user_id: {user_id}")

    if not user_id:
        logger.error("User ID is required")
        await websocket.close(code=403, reason="User ID is required")
        return
    
    await manager.connect(websocket, user_id)
    try:
        while True:
            # 클라이언트로부터 메시지 수신
            data = await websocket.receive_text()
            logger.info(f"Received message: {data}")

            # 메시지 처리 로직 (예: DB 저장, 텔레그램 전송 등)
            await manager.send_message_to_user(user_id, data)
    except WebSocketDisconnect:
        await manager.disconnect(user_id)
        logger.error(f"WebSocket connection closed: {user_id}")
    except Exception as e:
        logger.error(f"WebSocket error user_id: {user_id}, error: {e}")

