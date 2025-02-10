from typing import List
from sqlalchemy.orm import Session
from app.database.models import Post

class PostRepository:
    @staticmethod
    def create(db: Session, content: str, author_id: int) -> Post:
        """Создание поста"""
        new_post = Post(content=content, author_id=author_id)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post

    @staticmethod
    def get(db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
        return db.query(Post).offset(skip).limit(limit).all()