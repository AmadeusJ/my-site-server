from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import get_chat_messages
from app.schemas import ChatMessageList

router = APIRouter()

@router.post("/chat/messages", response_model=ChatMessageList)
async def get_messages(user_id: str, other_id: str, db: AsyncSession = Depends(get_db)):
    chat_messages = await get_chat_messages(db, user_id, other_id)
    return ChatMessageList(messages=chat_messages)
