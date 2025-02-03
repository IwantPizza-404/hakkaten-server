from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app.database.models import UserSession
from app.core.config import settings

class AuthRepository:
    @staticmethod
    def save_refresh_token(db: Session, user_id: int, token: str, device_id: str, ip: str, user_agent: str):
        """Сохраняем refresh-токен в БД"""
        db_token = UserSession(
            user_id=user_id,
            refresh_token=token,
            device_id=device_id,
            ip_address=ip,
            user_agent=user_agent,
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(db_token)
        db.commit()

    @staticmethod
    def revoke_refresh_token(db: Session, token: str):
        """Отзываем refresh-токен"""
        print(f"Полученный токен: {token}")
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
    def get_session_by_token(db: Session, token: str):
        """Ищем сессию по токену"""
        session = db.query(UserSession).filter(
            UserSession.refresh_token == token,
            UserSession.is_revoked == False,
            UserSession.expires_at > datetime.now(timezone.utc)
        ).first()
        return session
