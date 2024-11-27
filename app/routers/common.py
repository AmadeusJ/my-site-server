from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import get_statistic
from app.schemas import Statistic
from app.logger import logger
import os

router = APIRouter()


@router.get("/welcome")
async def welcome(db: AsyncSession = Depends(get_db)):
    """
    페이지 진입시 기본 데이터 반환 / N번째 방문자수 등
    """
    statistic = await get_statistic(db)
    return {"statistic": statistic}


@router.get("/status")
async def get_status():
    """
    서버와 Telegram 상태를 반환하는 API
    """
    try:
        # 서버 상태 (기본적으로 항상 'online')
        server_status = "online"

        # Telegram 상태 확인
        telegram_enabled = os.getenv("TELEGRAM_ENABLED", "false").lower() == "true"

        # 결과 반환
        logger.info("Server and Telegram status checked")
        return {
            "server": server_status,
            "telegram": "enabled" if telegram_enabled else "disabled"
        }
    except Exception as e:
        logger.error(f"Error while checking status: {e}")
        return {
            "server": "error",
            "telegram": "error"
        }
