from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    hashed = pwd_context.hash(password)
    print(f"🔒 Хешируем пароль: {password} -> {hashed}")
    return hashed

def verify_password(plain_password: str, hashed_password: str) -> bool:
    result = pwd_context.verify(plain_password, hashed_password)
    print(f"🔍 Проверка: {plain_password} -> {hashed_password} = {result}")
    return result
