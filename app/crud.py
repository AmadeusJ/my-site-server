from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Project, ChatMessage, Statistic
from app.schemas import ProjectCreate, ChatMessageCreate
from app.logger import logger

async def get_statistic(db: AsyncSession):
    statistic = await db.execute(select(Statistic))
    return statistic.scalars().all()

async def get_projects(db: AsyncSession, category: str):
    if category.lower() == 'all':
        projects = await db.execute(select(Project))
    else:
        projects = await db.execute(select(Project).where(Project.category == category))
    return projects.scalars().all()


async def get_project(db: AsyncSession, project_id: int):
    project = await db.get(Project, project_id)
    return project


async def create_project(db: AsyncSession, project: ProjectCreate):
    db_project = Project(**project.model_dump())
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project


async def create_chat_message(db: AsyncSession, chat_message: ChatMessageCreate):
    db_chat_message = ChatMessage(**chat_message.model_dump())
    db.add(db_chat_message)
    await db.commit()
    await db.refresh(db_chat_message)
    logger.info(f"Chat message created for {db_chat_message.sender_id} : {db_chat_message.content}")
    return db_chat_message


async def get_chat_messages(db: AsyncSession, user_id: str, other_id: str):
    chat_messages = await db.execute(
        select(ChatMessage).where(
            (
                (ChatMessage.sender_id == user_id) & 
                (ChatMessage.receiver_id == other_id)
            ) |
            (
                (ChatMessage.sender_id == other_id) & 
                (ChatMessage.receiver_id == user_id)
            )
        ).order_by(ChatMessage.created_at.desc())
    )
    return chat_messages.scalars().all()

