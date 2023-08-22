import os

from pydantic import BaseSettings


class TortoiseSettings(BaseSettings):
    db_url: str
    modules: dict
    generate_schemas: bool

    class Config:
        env_file = f"{os.path.dirname(os.path.abspath(__name__))}\\.env"
        env_file_encoding = "utf-8"


class OpenAPISettings(BaseSettings):
    app_name: str
    version: str
    description: str

    class Config:
        env_file = f"{os.path.dirname(os.path.abspath(__name__))}\\.env"
        env_file_encoding = "utf-8"


tortoise_config = TortoiseSettings()
openapi_config = OpenAPISettings()
