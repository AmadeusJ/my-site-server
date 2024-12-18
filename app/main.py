from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from werkzeug.middleware.proxy_fix import ProxyFix
from app.models import Base
from app.database import engine
from app.routers import common, websocket, chat, telegram_hook, email
from app.logger import logger
from telegram.ext import ApplicationBuilder
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # 서버에서 공개할 HTTPS URL
WEBHOOK_PATH = "/telegram/webhook"

# Telegram 애플리케이션 생성
telegram_application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()


@asynccontextmanager
async def lifespan(app: FastAPI):
        # Telegram Webhook 설정
    try:
        await telegram_application.bot.set_webhook(url=WEBHOOK_URL + WEBHOOK_PATH)
        logger.info(f"Telegram webhook 설정 완료: {WEBHOOK_URL + WEBHOOK_PATH}")
    except Exception as e:
        logger.error(f"Telegram webhook 설정 실패: {str(e)}")
        # Telegram 설정에 실패해도 API 서버는 실행해야 하므로 예외를 잡고 진행합니다.
        logger.warning("Telegram Webhook 설정 실패. 계속 진행합니다...")

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

# Docker Compose에서 전달된 ENVIRONMENT 환경 변수 읽기 (기본값: development)
environment = os.getenv("ENVIRONMENT", "development")

# Production 환경에서만 미들웨어 추가
if environment == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["dawoonjung.com", "www.dawoonjung.com", "*.dawoonjung.com"],
    )
    app.add_middleware(
        ProxyFix,
        x_for=1,
        x_proto=1,
        x_host=1,
        x_prefix=1,
    )

app.include_router(websocket.router, prefix="/ws", tags=["websocket"])
app.include_router(common.router, prefix="/api", tags=["common"])
# app.include_router(project.router, prefix="/api", tags=["project"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(telegram_hook.router, prefix="/telegram", tags=["telegram_hook"])
app.include_router(email.router, prefix="/api", tags=["email"])

logger.info("API Server started successfully.")