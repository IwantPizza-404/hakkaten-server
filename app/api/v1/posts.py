from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.post import PostCreate, PostResponse
from app.services.post import PostService
from app.database.session import get_db
from app.core.deps import get_current_user

router = APIRouter()

@router.post("/posts", response_model=PostResponse)
def create_post(
    post_data: PostCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return PostService.create(db, post_data, author_id=current_user.id)

@router.get("/posts", response_model=list[PostResponse])
def read_posts(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return PostService.get(db, skip, limit)