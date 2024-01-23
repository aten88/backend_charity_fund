from pydantic import BaseSettings


class Settings(BaseSettings):
    """ Класс с настройками приложения. """
    app_title: str
    app_description: str

    class Config:
        """ Подкласс конфигурации. """
        env_file = '.env'


settings = Settings()
