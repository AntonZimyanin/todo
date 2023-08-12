import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from todo.api.handlers import user_router


async def main(): 
    app = FastAPI()

    app.mount("/static", StaticFiles(directory="todo/static"), name="static")
    app.include_router(router=user_router)

    config = uvicorn.Config(app, port=8080, log_level="info")
    server = uvicorn.Server(config=config)
    
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
