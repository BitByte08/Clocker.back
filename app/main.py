# main.py
from fastapi import FastAPI
from database import init_db
from users.router import router as users_router
from teams.router import router as teams_router
from schedules.router import router as schedules_router
from auth.router import router as auth_router
import uvicorn

init_db()
app = FastAPI(title="Clocker API")

# 각 도메인 router 등록
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(teams_router, prefix="/teams", tags=["Teams"])
app.include_router(schedules_router, prefix="/schedules", tags=["Schedules"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",      # "파일명:FastAPI객체명"
        host="0.0.0.0",  # 컨테이너 외부에서 접속 가능
        port=8000,
        reload=True      # 개발 모드에서 코드 변경 시 자동 재시작
    )