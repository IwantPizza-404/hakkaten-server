from fastapi import Response, Request, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.repositories.user import UserRepository
from app.repositories.auth import AuthRepository
from app.core.jwt import create_access_token, create_refresh_token
from app.core.hashing import verify_password

class AuthService:
    @staticmethod
    def login(request: Request, response: Response, db: Session, username_or_email: str, password: str):
        """Логин + создание refresh-токена"""
        user = UserRepository.get_by_email_or_username(db, username_or_email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        access_token = create_access_token(str(user.id))
        refresh_token = create_refresh_token(str(user.id))

        # 🛡 Привязываем токен к устройству и IP
        AuthRepository.save_refresh_token(
            db, user.id, refresh_token,
            request.headers.get("Device-Id", "unknown_device"),
            request.client.host,
            request.headers.get("User-Agent")
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="Lax",
            path="/"
        )

        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    def refresh(response: Response, db: Session, request: Request):
        """Обновление access_token"""
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token or not AuthRepository.is_refresh_token_valid(db, refresh_token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        session = AuthRepository.get_session_by_token(db, refresh_token) #Убрать преоброзователь при миграции на PostgreSQL
        if not session or session.is_revoked or session.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

        # Создаем новые токены
        new_access_token = create_access_token(str(session.user_id))
        new_refresh_token = create_refresh_token(str(session.user_id))

        # Обновляем refresh-токен в базе
        AuthRepository.revoke_refresh_token(db, refresh_token)
        AuthRepository.save_refresh_token(
            db, session.user_id, new_refresh_token,
            request.headers.get("Device-Id", "unknown_device"),
            request.client.host,
            request.headers.get("User-Agent")
        )

        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=False,
            secure=True,
            samesite="Lax",
            path="/"
        )

        return {"access_token": new_access_token, "token_type": "bearer"}

    @staticmethod
    def logout(response: Response, db: Session, request: Request):
        """Выход из системы (удаление refresh-токена)"""
        refresh_token = request.cookies.get("refresh_token")
        
        if refresh_token:
            AuthRepository.revoke_refresh_token(db, refresh_token)

        response.delete_cookie("refresh_token")
        return {"message": "Logout successful"}
