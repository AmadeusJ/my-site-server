from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import get_chat_messages
from app.schemas import ResponseModel, ChatMessageListRequestSchema, ChatMessageListSchema
from app.utils.session import get_or_create_session

router = APIRouter()

@router.post("/chat/messages", response_model=ResponseModel)
async def get_messages(data: ChatMessageListRequestSchema, db: AsyncSession = Depends(get_db)):
    try:
        chat_messages = await get_chat_messages(data.user_id, db)
        return ResponseModel(status="success", data=chat_messages, message="채팅 메시지 조회 성공")
    except Exception as e:
        return ResponseModel(status="error", data=None, message=str(e))
