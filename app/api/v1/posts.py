from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import post, user
from app.repositories.post import PostRepository
from app.database.session import get_db
from app.core.deps import get_current_user

router = APIRouter()

@router.post("/posts", response_model=post.PostResponse)
def create_post(
    post: post.PostCreate,
    db: Session = Depends(get_db),
    current_user: user.UserResponse = Depends(get_current_user)
):
    return PostRepository.create(db, post, current_user.id)

@router.get("/posts", response_model=list[post.PostResponse])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return PostRepository.get(db, skip, limit)