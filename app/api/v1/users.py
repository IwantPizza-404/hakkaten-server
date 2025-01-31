from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import user
from app.services.user import UserService
from app.api.deps import get_db, get_current_user

router = APIRouter()

@router.post("/register", response_model = user.UserResponse)
def create_user(
    user_in: user.UserCreate,
    db: Session = Depends(get_db)
):
    user = UserService.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return UserService.create_user(db=db, user=user_in)

@router.get("/me", response_model = user.UserResponse)
def read_current_user(
    current_user: user.UserResponse = Depends(get_current_user)
):
    return current_user