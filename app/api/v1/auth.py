from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database.session import get_db
from app.services.auth import AuthService
from app.services.user import UserService
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""
    return UserService.register(db, user_data)

@router.post("/login", response_model=Token)
def login(
    request: Request,
    response: Response,  
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return AuthService.login(request, response, db, form_data.username, form_data.password)

@router.post("/refresh", response_model=Token)
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    """Обновление access-токена"""
    return AuthService.refresh(response, db, request)

@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    """Выход из системы"""
    return AuthService.logout(response, db, request)
