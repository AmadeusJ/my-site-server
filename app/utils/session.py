from datetime import datetime
from app.models import Session
from sqlalchemy.ext.asyncio import AsyncSession

async def get_or_create_session(user_id: str, db: AsyncSession):
    # 세션 검색
    session = await db.query(Session).filter(Session.user_id == user_id).first()
    if session:
        # 세션이 존재하면 반환
        return session

    # 세션이 없으면 새로 생성
    new_session = Session(
        user_id=user_id,
        created_at=datetime.now(datetime.timezone.utc),
        last_message_date=datetime.now(datetime.timezone.utc),
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session
