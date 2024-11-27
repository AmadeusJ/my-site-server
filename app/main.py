from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import Base
from app.database import engine
from app.routers import portfolio, websocket
from app.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # 시작할 때 실행
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("데이터베이스 테이블 생성 완료")
    except Exception as e:
        # 개발 환경에서는 DB 연결 실패해도 계속 진행
        logger.warning(f"데이터베이스 초기화 실패: {str(e)}")
        logger.warning("DB 없이 API 서버를 시작합니다.")
    
    yield
    # 종료할 때 실행 (필요한 경우)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(portfolio.router, prefix="/api", tags=["portfolio"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])

logger.info("API Server started successfully.")