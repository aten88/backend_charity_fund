from pydantic import BaseSettings


class Settings(BaseSettings):
    """ Класс с настройками приложения. """
    app_title: str
    app_description: str
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    class Config:
        """ Подкласс конфигурации. """
        env_file = '.env'


settings = Settings()
