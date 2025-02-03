import jwt
from datetime import datetime, timedelta
from app.core.config import settings
from app.schemas.token import TokenPayload

def create_access_token(subject: str) -> str:
    """Создаёт access-токен"""
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": subject, "exp": expire}
    
    token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode()
    return token

def create_refresh_token(subject: str) -> str:
    """Создаёт refresh-токен"""
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"sub": subject, "exp": expire}

    token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode()
    return token

def decode_access_token(token: str) -> TokenPayload:
    """Декодирует access-токен"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

def verify_refresh_token(token: str) -> str:
    """Проверяет refresh-токен и возвращает user_id"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Refresh token payload missing user ID")
        return user_id
    except jwt.ExpiredSignatureError:
        raise ValueError("Refresh token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid refresh token")

