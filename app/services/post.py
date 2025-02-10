from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.post import PostRepository
from app.schemas.post import PostCreate

class PostService:
    @staticmethod
    def create(db: Session, post_data: PostCreate, author_id: int):
        """Создает новый пост"""
        if not author_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return PostRepository.create(db, post_data.content, author_id)
    
    @staticmethod
    def get(db: Session, skip: int = 0, limit: int = 100, ):
        """Получает посты"""

        return PostRepository.get(db, skip, limit)