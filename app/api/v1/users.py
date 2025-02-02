from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.core.security import get_current_user
from app.repositories.user import UserRepository
from app.schemas.user import UserResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/me", response_model=UserResponse)
def get_my_info(
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = UserRepository.get_by_id(db, current_user_id)
    return user