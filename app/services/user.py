from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.core.hashing import get_password_hash

class UserService:
    @staticmethod
    def register(db: Session, user_data: UserCreate):
        """Регистрирует нового пользователя"""
        existing_user = UserRepository.get_by_email_or_username(db, user_data.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

        hashed_password = get_password_hash(user_data.password)

        new_user_data = UserCreate(
            email=user_data.email,
            username=user_data.username,
            password=hashed_password,
            full_name=user_data.full_name 
        )

        new_user = UserRepository.create(db, new_user_data)
        return new_user
