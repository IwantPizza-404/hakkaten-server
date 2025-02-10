from pydantic_settings import BaseSettings
# from pydantic import Field

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"  # Префикс для API
    JWT_SECRET_KEY: str              # Секретный ключ для JWT
    JWT_ALGORITHM: str = "HS256"     # Алгоритм шифрования JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # Время жизни access-token
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # Время жизни refresh-token
    DATABASE_URL: str            # URL базы данных (например, PostgreSQL)

    class Config:
        env_file = ".env"  # Загрузка переменных из файла .env

settings = Settings()  # Экземпляр конфигурации