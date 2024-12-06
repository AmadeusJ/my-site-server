from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import get_chat_messages
from app.schemas import ChatMessageListRequestSchema, ChatMessageListSchema

router = APIRouter()

@router.post("/chat/messages", response_model=ChatMessageListSchema)
async def get_messages(data: ChatMessageListRequestSchema, db: AsyncSession = Depends(get_db)):
    chat_messages = await get_chat_messages(db, data.user_id)
    return ChatMessageListSchema(**chat_messages)
