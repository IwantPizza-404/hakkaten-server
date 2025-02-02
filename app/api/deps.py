from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings
<<<<<<< HEAD
from app.services.user import UserService
=======
from app.repositories.user import UserRepository
from app.schemas.auth import TokenData
>>>>>>> 4c0d81b (update)
from app.database.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        # Convert user_id from string to integer
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception
    
    user = UserRepository.get_by_id(db, user_id=user_id)
    if user is None:
        raise credentials_exception
    return user