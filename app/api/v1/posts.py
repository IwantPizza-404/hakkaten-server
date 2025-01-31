from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import post, user
from app.services.post import PostService
from app.api.deps import get_db, get_current_user

router = APIRouter()

@router.post("/posts", response_model=post.PostResponse)
def create_post(
    post: post.PostCreate,
    db: Session = Depends(get_db),
    current_user: user.UserResponse = Depends(get_current_user)
):
    return PostService.create_post(db, post, current_user.id)

@router.get("/posts", response_model=list[post.PostResponse])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return PostService.get_posts(db, skip, limit)