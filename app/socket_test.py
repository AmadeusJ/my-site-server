from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import logging

app = FastAPI()
logger = logging.getLogger("websocket_test")
logging.basicConfig(level=logging.INFO)

@app.websocket("/ws/test")
async def websocket_test(websocket: WebSocket):
    logger.info("WebSocket connection received")
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            logger.info(f"Received message: {message}")
            await websocket.send_text(f"Echo: {message}")
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
