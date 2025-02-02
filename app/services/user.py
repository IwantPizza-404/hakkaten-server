from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.core.hashing import verify_password
from app.core.jwt import create_access_token

class UserService:
    @staticmethod
    def register_user(db: Session, user_in: UserCreate):
        # Проверка существующего пользователя
        existing_user = UserRepository.get_by_email(db, user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        # Создание
        return UserRepository.create(db, user_in)

    @staticmethod
    def authenticate(db: Session, username_or_email: str, password: str):
        # Поиск пользователя по email, если не найден - по username
        user = UserRepository.get_by_email(db, username_or_email)
        if not user:
            user = UserRepository.get_by_username(db, username_or_email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        return user

    @staticmethod
    def login(db: Session, username_or_email: str, password: str):
        user = UserService.authenticate(db, username_or_email, password)
        access_token = create_access_token(str(user.id))
        return {"access_token": access_token, "token_type": "bearer"}
