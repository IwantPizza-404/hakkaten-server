import logging
from datetime import datetime, timedelta
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from app.repositories.post import PostRepository
from app.core.upload import upload_image

# Логгер для отслеживания ошибок
logger = logging.getLogger(__name__)

POST_INTERVAL = timedelta(seconds=30)

class PostService:
    @staticmethod
    def create(db: Session, content: str, author_id: int, image: UploadFile = None):
        """Создание нового поста"""

        if not author_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Not authorized"
            )
        
        last_post = PostRepository.get_last_post_by_user(db, author_id)
        if last_post and datetime.utcnow() - last_post.created_at < POST_INTERVAL:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Server is busy, try later"
            )
        
        if not (10 <= len(content) <= 5000):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Длина поста должна быть от 10 до 5000 символов"
            )

        content = content.strip()
        image_url = None

        if image:
            try:
                image_url = upload_image(image)
                if isinstance(image_url, dict):
                    image_url = image_url.get("url") 
            except Exception as e:
                logger.error(f"Ошибка при загрузке изображения: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Ошибка при загрузке изображения"
                )

        try:
            return PostRepository.create(db, content, author_id, image_url)
        except Exception as e:
            logger.error(f"Ошибка при создании поста: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при создании поста"
            )
    
    @staticmethod
    def get(db: Session, skip: int = 0, limit: int = 100):
        """Получение постов"""

        try:
            return PostRepository.get(db, skip, limit)
        except Exception as e:
            logger.error(f"Ошибка при получении постов: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при получении постов"
            )
