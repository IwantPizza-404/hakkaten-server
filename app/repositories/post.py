from typing import List
from sqlalchemy.orm import Session
from app.database.models import Post
from app.schemas.post import PostCreate

class PostRepository:
    @staticmethod
    def create(db: Session, post: PostCreate, author_id: int) -> Post:
        db_post = Post(content=post.content, author_id=author_id)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post

    @staticmethod
    def get(db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
        return db.query(Post).offset(skip).limit(limit).all()