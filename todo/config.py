import os

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    app_name: SecretStr
    db_url: SecretStr

    class Config:
        env_file = f"{os.path.dirname(os.path.abspath(__name__))}\\.env"
        env_file_encoding = "utf-8"


config = Settings()
