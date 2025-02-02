from fastapi import Response, Request, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.repositories.user import UserRepository
from app.core.jwt import create_access_token, create_refresh_token
from app.core.hashing import verify_password
from app.database.models import UserSession

class AuthService:
    @staticmethod
    def login(request: Request, response: Response, db: Session, username_or_email: str, password: str):
        """Логин + создание refresh-токена"""
        user = UserRepository.get_by_email_or_username(db, username_or_email)

        if not user:
            print(f"❌ Пользователь '{username_or_email}' не найден в базе!")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        print(f"🔎 Проверка пароля для пользователя: {user.username}")
        print(f"✅ Хешированный пароль в БД: {user.hashed_password}")

        if not verify_password(password, user.hashed_password):
            print("❌ Пароль не совпадает!")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        print("✅ Пароль совпадает, выдаем токен!")


        access_token = create_access_token(str(user.id))
        refresh_token = create_refresh_token(str(user.id))

        # 🛡 Привязываем токен к устройству и IP
        device_id = request.headers.get("Device-Id", "unknown_device")
        ip_adress = request.client.host
        user_agent = request.headers.get("User-Agent")
        UserRepository.save_refresh_token(db, user.id, refresh_token, device_id, ip_adress, user_agent)

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
        if not refresh_token or not UserRepository.is_refresh_token_valid(db, refresh_token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        session = db.query(UserSession).filter(UserSession.refresh_token == refresh_token).first()
        if session.is_revoked or session.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

        new_access_token = create_access_token(session.user_id)
        new_refresh_token = create_refresh_token(session.user_id)

        # Удаляем старый refresh_token и создаем новый
        UserRepository.revoke_refresh_token(db, refresh_token)
        UserRepository.save_refresh_token(db, session.user_id, new_refresh_token, request.client.host, request.headers.get("User-Agent"))

        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
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
            UserRepository.revoke_refresh_token(db, refresh_token)

        response.delete_cookie("refresh_token")
        return {"message": "Logout successful"}
