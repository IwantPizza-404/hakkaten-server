from typing import List
from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate

class PostService:
    @staticmethod
    def create_post(db: Session, post: PostCreate, author_id: int) -> Post:
        db_post = Post(content=post.content, author_id=author_id)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post

    @staticmethod
    def get_posts(db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
        return db.query(Post).offset(skip).limit(limit).all()