from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Habit"
    SERVER_HOST: str
    SERVER_PORT: int
    DB_NAME: str
    DB_URL: str
    CLIENT_ID: str
    CLIENT_SECRET: str

    class Config:
        env_file = ".env"


settings = Settings()
