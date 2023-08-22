import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from todo.api.handlers import user_router
from todo.database.initializer import init_db
from todo.config import openapi_config


async def main():
    app = FastAPI(
        title=openapi_config.app_name,
        version=openapi_config.version,
        description=openapi_config.description,
    )

    init_db(app)
    app.mount("/static", StaticFiles(directory="todo/static"), name="static")
    app.include_router(router=user_router)

    config = uvicorn.Config(app, port=8080, log_level="info")
    server = uvicorn.Server(config=config)

    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
