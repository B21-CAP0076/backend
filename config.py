from pydantic import BaseSettings
import os


class GeneralSettings(BaseSettings):
    APP_NAME: str = "Habit"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    SERVER_HOST: str = os.environ.get("SERVER_HOST")
    SERVER_PORT: int = os.environ.get("SERVER_PORT")


class DatabaseSettings(BaseSettings):
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_URL: str = os.environ.get("DB_URL")


class Settings(GeneralSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
