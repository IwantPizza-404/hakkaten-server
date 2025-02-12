from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.post import PostRepository
from app.schemas.post import PostCreate

class PostService:
    @staticmethod
    def create(db: Session, post_data: PostCreate, author_id: int):
        """Создание нового поста"""
        if not author_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неавторизованный пользователь")
        
        if not post_data.content or len(post_data.content.strip()) < 10:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пост должен содержать хотя бы 10 символов")
        elif not post_data.content or len(post_data.content.strip()) > 5000:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пост должен содержать хотя бы 10 символов")

        # Фильтрация
        banned_words = ["Негр", "Сука", "Жаляп"]
        if any(word in post_data.content.lower() for word in banned_words):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ваш пост содержит запрещенные слова")

        try:
            return PostRepository.create(db, post_data.content, author_id)
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при создании поста")
    
    @staticmethod
    def get(db: Session, skip: int = 0, limit: int = 100, ):
        """Получение постов"""

        try:
            return PostRepository.get(db, skip, limit)
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при получении постов")