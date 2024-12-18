from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import ChatMessage, Statistic, Session
from app.schemas import ChatMessageCreateSchema, SessionSchema, StatisticSchema
from app.logger import logger
from datetime import datetime
from app.globals import SEOUL_TIMEZONE 
from pydantic import parse_obj_as


async def get_statistic(user_id: str, isNewVisitor: bool, db: AsyncSession):
    """
    방문자 통계 조회 및 업데이트
    """
    try:
        statistic_result = await db.execute(select(Statistic))
        statistic = statistic_result.scalars().first()

        # 통계가 없으면 초기화 (에러를 방지하기 위해)
        if not statistic:
            statistic = Statistic(total_count=0, last_updated_at=datetime.now(SEOUL_TIMEZONE))
            db.add(statistic)
            await db.flush()  # 통계 추가 후 영속화

        # 새로운 방문자인 경우
        if isNewVisitor:
            statistic.total_count += 1
            statistic.last_updated_at = datetime.now(SEOUL_TIMEZONE)

        # 세션 조회 및 업데이트
        session_result = await db.execute(select(Session).where(Session.user_id == user_id))
        session = session_result.scalars().first()
        if session:
            # 세션이 존재하면 반환
            session.last_updated_at = datetime.now(SEOUL_TIMEZONE)
        else:
            # 세션이 없으면 새로 생성
            new_session = Session(
                user_id=user_id,
                created_at=datetime.now(SEOUL_TIMEZONE),
                last_updated_at=datetime.now(SEOUL_TIMEZONE),
            )
            db.add(new_session)
            await db.flush()

        await db.commit()

        # ORM 객체를 딕셔너리로 변환하여 반환
        statistic_dict = {
            "id": statistic.id,
            "total_count": statistic.total_count,
            "last_updated_at": statistic.last_updated_at
        }
        return statistic_dict
    
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Statistic CRUD 에러입니다ㅜㅜ...: {e}")
        raise e


async def create_chat_message(session_id: int, chat_message: dict, is_sent_to_telegram: bool, db: AsyncSession):
    chat_message = parse_obj_as(ChatMessageCreateSchema, chat_message)
    db_chat_message = ChatMessage(**chat_message.model_dump())
    db_chat_message.session_id = session_id
    db_chat_message.is_sent_to_telegram = is_sent_to_telegram
    db_chat_message.created_at = datetime.now(SEOUL_TIMEZONE)
    db.add(db_chat_message)
    await db.commit()
    await db.refresh(db_chat_message)

    chat_message_dict = {
        "id": db_chat_message.id,
        "sender_id": db_chat_message.sender_id,
        "content": db_chat_message.content,
        "created_at": db_chat_message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "is_sent_to_telegram": db_chat_message.is_sent_to_telegram
    }
    logger.info(f"Chat message created for {db_chat_message.sender_id} : {chat_message_dict}")

    return chat_message_dict


async def get_chat_messages(user_id: str, db: AsyncSession):
    try:
        chat_messages = await db.execute(
            select(ChatMessage)
            .join(Session, ChatMessage.session_id == Session.id)
            .where(Session.user_id == user_id)
            .order_by(ChatMessage.created_at.asc())
        )

        # ORM 객체를 딕셔너리로 변환하여 반환
        chat_messages_dict = {
            "user_id": user_id,
            "messages": [message.to_dict() for message in chat_messages.scalars().all()]
        }
        return chat_messages_dict
    except SQLAlchemyError as e:
        logger.error(f"Chat messages CRUD 에러입니다ㅜㅜ...: {e}")
        raise e


# async def get_projects(db: AsyncSession, category: str):
#     if category.lower() == 'all':
#         projects = await db.execute(select(Project))
#     else:
#         projects = await db.execute(select(Project).where(Project.category == category))
#     return projects.scalars().all()


# async def get_project(db: AsyncSession, project_id: int):
#     project = await db.get(Project, project_id)
#     return project


# async def create_project(db: AsyncSession, project: ProjectCreate):
#     db_project = Project(**project.model_dump())
#     db.add(db_project)
#     await db.commit()
#     await db.refresh(db_project)
#     return db_project
