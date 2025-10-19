# users/crud.py
from sqlalchemy.orm import Session
from models import User

def create_user(db: Session, name: str, password_hash: str):
    user = User(name=name, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()
