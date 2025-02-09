import os

from pydantic import BaseSettings

class Settings(BaseSettings):
    # Настройки подключения к БД
    DATABASE_URL: str = "postgresql+psycopg2://app_user:app_pass@localhost:5432/app_db"

    # JWT
    JWT_SECRET_KEY: str = "SUPER_SECRET_JWT_KEY"  
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # сколько минут жить токену

    # Секретный ключ для формирования подписи платёжного вебхука
    SIGNATURE_SECRET_KEY: str = "gfdmhghif38yrf9ew0jkf32"

    # Начальные данные для пользователей в миграции
    ADMIN_EMAIL: str = "admin@example.com"
    ADMIN_PASSWORD: str = "adminpass"

    USER_EMAIL: str = "user@example.com"
    USER_PASSWORD: str = "userpass"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings(
    _env_file=None,  # Если хотим подгружать из .env, то указываем ".env"
    _env_file_encoding="utf-8"
)