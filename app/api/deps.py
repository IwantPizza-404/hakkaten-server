from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings
from app.repositories.user import UserRepository
from app.schemas.auth import TokenData
from app.database.session import get_db
from app.core.jwt import decode_access_token, verify_refresh_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """Получает текущего пользователя по access-токену"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id: str = payload.sub
    except JWTError:
        raise credentials_exception

    user = UserRepository.get_by_id(db, user_id=user_id)
    if not user:
        raise credentials_exception
    return user


def get_current_user_from_refresh_token(
    request: Request, 
    db: Session = Depends(get_db)
):
    """Получает пользователя по refresh-токену из cookies"""
    
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")

    try:
        user_id = verify_refresh_token(refresh_token)
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    user = UserRepository.get_by_id(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user
