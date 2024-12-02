# 베이스 이미지
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# Poetry 설치
RUN pip install --no-cache-dir poetry

# 프로젝트 파일 복사
COPY pyproject.toml poetry.lock ./

# Poetry로 의존성 설치
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# 애플리케이션 코드 복사
COPY . .

# FastAPI 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
