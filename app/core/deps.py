from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.repositories.user import UserRepository
from app.database.session import get_db
from app.core.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """Получает текущего пользователя по access-токену"""
    payload = decode_access_token(token)
    user_id: str = payload.sub

    user = UserRepository.get_by_id(db, user_id=user_id)
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive or not found",
        )
    
    return user
