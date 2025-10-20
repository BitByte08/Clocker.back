# main.py
from fastapi import FastAPI
from database import init_db
from users.router import router as users_router
from teams.router import router as teams_router
from schedules.router import router as schedules_router
from auth.router import router as auth_router
import uvicorn

# DB 초기화
init_db()

# FastAPI 앱 생성, docs/openapi 경로를 /api 기준으로 설정
app = FastAPI(
    title="Clocker API",
    docs_url="/api/docs",           # Swagger UI
    redoc_url="/api/redoc",         # ReDoc
    openapi_url="/api/openapi.json" # OpenAPI JSON
)

# 각 도메인 router 등록, 전체 prefix /api로 이동
app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(teams_router, prefix="/api/teams", tags=["Teams"])
app.include_router(schedules_router, prefix="/api/schedules", tags=["Schedules"])
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",      # "파일명:FastAPI객체명"
        host="0.0.0.0",  # 외부 접속 가능
        port=8000,
        reload=True      # 개발 모드 자동 재시작
    )
