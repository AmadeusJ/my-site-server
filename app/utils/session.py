from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.globals import SEOUL_TIMEZONE
from app.models import Session

async def get_or_create_session(user_id: str, db: AsyncSession):
    """
    세션 조회 및 생성
    """
    # 세션 검색
    session_result = await db.execute(select(Session).where(Session.user_id == user_id))
    session = session_result.scalars().first()
    if session:
        # 세션이 존재하면 반환
        return session

    # 세션이 없으면 새로 생성
    new_session = Session(
        user_id=user_id,
        created_at=datetime.now(SEOUL_TIMEZONE),
        last_updated_at=datetime.now(SEOUL_TIMEZONE),
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)

