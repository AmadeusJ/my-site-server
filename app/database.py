import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.logger import logger
# .env 파일 로드
load_dotenv()

# 환경 변수 설정
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DRIVER = os.getenv("DB_DRIVER")

# 데이터베이스 URL 동적으로 생성
DATABASE_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

if not DATABASE_URL:
    raise ValueError("DATABASE_URL을 생성할 수 없습니다. 환경 변수를 확인하세요.")

logger.info(f"Connecting to database at {DB_HOST}:{DB_PORT}")

# 비동기 엔진 생성
# engine = create_async_engine(DATABASE_URL, echo=True, pool_size=10, max_overflow=20)
engine = create_async_engine(DATABASE_URL, echo=True)

# 세션 매퍼 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# 의존성 주입용 함수
async def get_db():
  logger.info("Database session opened")
  async with SessionLocal() as session:
        yield session
  logger.info("Database session closed")
