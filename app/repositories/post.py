from typing import List, Optional
from sqlalchemy.orm import Session
from app.database.models import Post

class PostRepository:
    @staticmethod
    def create(db: Session, content: str, author_id: int, image: Optional[str] = None) -> Post:
        """Создание поста"""
        new_post = Post(
            content=content, 
            author_id=author_id,
            image_url=image or None
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post

    @staticmethod
    def get(db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
        return db.query(Post).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_last_post_by_user(db: Session, user_id: int):
        """Получает последний пост пользователя"""
        return (
            db.query(Post)
            .filter(Post.author_id == user_id)
            .order_by(Post.created_at.desc())
            .first()
        )