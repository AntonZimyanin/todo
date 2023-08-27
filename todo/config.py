import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str
    db_url: str

    class Config:
        env_file = f"{os.path.dirname(os.path.abspath(__name__))}/.env"
        env_file_encoding = "utf-8"


config = Settings()
