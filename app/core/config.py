from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """ Класс с настройками приложения. """
    app_title: str
    app_description: str
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        """ Подкласс конфигурации. """
        env_file = '.env'


settings = Settings()
