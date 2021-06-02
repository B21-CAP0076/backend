from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Habit"
    DEBUG_MODE: bool = True
    SERVER_HOST: str
    SERVER_PORT: int
    DB_NAME: str
    DB_URL: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    DB_USER_COLLECTION: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
