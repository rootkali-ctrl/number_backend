from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str
    DB_NAME: str = "tsdb-users-dev"

    class Config:
        env_file = ".env"


settings = Settings()
