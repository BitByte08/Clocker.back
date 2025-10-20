from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import User
from core.security import hash_password, verify_password

def create_user(db: Session, name: str, password: str):
    """회원가입: 비밀번호 해시 저장"""
    existing_user = db.query(User).filter(User.name == name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = hash_password(password)
    user = User(name=name, password_hash=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, name: str, password: str):
    """로그인: 사용자 인증"""
    user = db.query(User).filter(User.name == name).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user
