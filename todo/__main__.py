import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from todo.api.handlers import (
    auth_router,
    admin_router,
    profile_router, 
    todo_router 
)


async def main():
    app = FastAPI()

    app.mount("/static", StaticFiles(directory="todo/static"), name="static")
    app.include_router(router=auth_router)
    app.include_router(router=admin_router)
    app.include_router(router=profile_router)
    app.include_router(router=todo_router)


    config = uvicorn.Config(app, port=8000, log_level="info")
    server = uvicorn.Server(config=config)

    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
