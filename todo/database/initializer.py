from fastapi import FastAPI
from tortoise.contrib.starlette import register_tortoise

from todo.config import tortoise_config


def init_db(app: FastAPI) -> None:
    """
    Init database models.
    :param app:
    :return:
    """

    register_tortoise(
        app,
        db_url=tortoise_config.db_url,
        modules=tortoise_config.modules,
        generate_schemas=tortoise_config.schema,
    )
