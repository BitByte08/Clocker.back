from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from core import security
from . import schemas, crud
from database import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# 회원가입
@router.post("/signup", response_model=schemas.UserRead)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user.name, user.password)

# ✅ 로그인 → Access 토큰은 응답 JSON으로, Refresh 토큰은 쿠키로
@router.post("/login", response_model=schemas.Token)
def login(response: Response, credentials: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, credentials.name, credentials.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # access_token (15분), refresh_token (7일)
    access_token = security.create_access_token({"sub": user.name}, expires_delta=timedelta(minutes=15))
    refresh_token = security.create_refresh_token({"sub": user.name}, expires_delta=timedelta(days=7))

    # Refresh Token은 HttpOnly 쿠키에 저장
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=604800,  # 7일
        samesite="lax",
        secure=False  # HTTPS 시 True
    )

    # Access Token은 JSON으로 반환 (프론트엔드가 Authorization 헤더에 넣을 것)
    return {"access_token": access_token, "token_type": "bearer"}


# ✅ /refresh → Refresh 쿠키 검증 후 새 Access 토큰 반환
@router.post("/refresh", response_model=schemas.Token)
def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    payload = security.verify_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid payload")

    new_access_token = security.create_access_token({"sub": username}, expires_delta=timedelta(minutes=15))
    return {"access_token": new_access_token, "token_type": "bearer"}


# ✅ 로그아웃 → Refresh 쿠키 삭제
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}
# 현재 로그인한 사용자 조회
@router.get("/me", response_model=schemas.UserRead)
def read_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = security.verify_token(token)
    username: str = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    user = db.query(crud.User).filter(crud.User.name == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
