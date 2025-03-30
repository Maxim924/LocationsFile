from dotenv import dotenv_values
from pydantic_settings import BaseSettings

env_values = dotenv_values(".env")

class Settings(BaseSettings):
    ASYNC_DATABASE_URL: str = env_values.get("ASYNC_DATABASE_URL")
    DATABASE_URL: str = env_values.get("DATABASE_URL")

settings = Settings()
