from typing import Optional
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.models import User, UserSession
from app.schemas.user import UserCreate

class UserRepository:
    @staticmethod
    def create(db: Session, user_in: UserCreate) -> User:
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=user_in.password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def save_refresh_token(db: Session, user_id: int, token: str, device_id: str, ip: str, user_agent: str):
        """Сохраняем refresh-токен в БД"""
        db_token = UserSession(
            user_id=user_id,
            refresh_token=token,
            device_id=device_id,
            ip_address=ip,
            user_agent=user_agent,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7)
        )
        db.add(db_token)
        db.commit()

    @staticmethod
    def revoke_refresh_token(db: Session, token: str):
        """Отзываем refresh-токен"""
        rows_updated = db.query(UserSession).filter(UserSession.refresh_token == token).update({"is_revoked": True})
        print(f"🔄 Обновлено строк: {rows_updated}")
        db.commit()
    
    @staticmethod
    def is_refresh_token_valid(db: Session, token: str) -> bool:
        """Проверяем, валиден ли refresh-токен"""
        session = db.query(UserSession).filter(
            UserSession.refresh_token == token,
            UserSession.is_revoked == False,
            UserSession.expires_at > datetime.now(timezone.utc)
        ).first()
        return bool(session)

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email_or_username(db: Session, username_or_email: str):
        print(f"🔎 Ищем пользователя: {username_or_email}")
        user = db.query(User).filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()
        print(f"✅ Найденный пользователь: {user}")
        return user
