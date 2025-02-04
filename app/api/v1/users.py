from fastapi import APIRouter, Depends
from app.core.deps import get_current_user
from app.schemas.user import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_my_info(
    current_user: dict = Depends(get_current_user),
):
    return current_user