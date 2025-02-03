from sqlalchemy.orm import Session
from app.database.models import User
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
