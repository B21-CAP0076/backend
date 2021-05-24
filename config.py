from pydantic import BaseSettings


class GeneralSettings(BaseSettings):
    APP_NAME: str = "Habit"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_NAME: str = "habit"
    DB_URL: str = "mongodb://localhost:27017/"


class Settings(GeneralSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
