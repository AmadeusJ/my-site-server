from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import ProjectList, ProjectDetail, ChatMessageCreate
from app.logger import logger
from app.utils.connection_manager import ConnectionManager
import os

router = APIRouter()

# 웹소켓 연결 관리자 인스턴스 생성
manager = ConnectionManager()


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


@router.get("/projects", response_model=ProjectList)
async def get_projects(db: AsyncSession = Depends(get_db)):
    projects = await db.execute(select(Portfolio))
    return ProjectList(projects=projects.scalars().all())


@router.get("/projects/{project_id}", response_model=ProjectDetail)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    project = await db.get(Portfolio, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectDetail(project=project)




# @router.post("/send_email")
# async def send_email(email: Email):
#     return await send_email(email)
