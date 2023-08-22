from typing import Annotated

from fastapi import Request, Depends, Form, APIRouter, Path
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_303_SEE_OTHER, HTTP_302_FOUND
from starlette.datastructures import URL

from todo.config import openapi_config
from todo.api.action.todo import (
    _select_all_todo,
    _create_todo,
    _update_todo,
    _delete_todo,
)

user_router = APIRouter()

templates = Jinja2Templates(directory="todo/templates")
templates.env.globals["URL"] = URL


@user_router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    todo_list = await _select_all_todo()

    return templates.TemplateResponse(
        "todo/index.html",
        {
            "request": request,
            "app_name": openapi_config.app_name,
            "todo_list": todo_list,
            "is_title": True,
        },
    )


@user_router.get("/nullable_title", response_class=HTMLResponse)
async def nullable_title(request: Request):
    todos = await _select_all_todo()
    return templates.TemplateResponse(
        "todo/index.html",
        {
            "request": request,
            "app_name": openapi_config.app_name,
            "todo_list": todos,
            "is_title": False,
        },
    )


@user_router.post("/add", response_class=RedirectResponse)
async def add(
    title: Annotated[str | None, Form(min_length=1)] = None,
):
    if title is not None:
        await _create_todo(title=title)
        url = user_router.url_path_for("home")
        return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
    else:
        url = user_router.url_path_for("nullable_title")
        return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@user_router.get("/update/{todo_id}/{is_complete}", response_class=RedirectResponse)
async def update(
    todo_id: int = Path(..., description="todo id"),
    is_complete: bool = Path(..., description="state todo"),
):
    update_todo = await _update_todo(
        todo_id=todo_id, params={"is_complete": is_complete}
    )
    if update_todo is not None:
        url = user_router.url_path_for("home")
        return RedirectResponse(url=url, status_code=HTTP_302_FOUND)
    else:
        raise HTTPException(
            status_code=404, detail=f"Todo with id {todo_id} not found."
        )


@user_router.get("/delete/{todo_id}", response_class=RedirectResponse)
async def delete(
    todo_id: int = Path(..., description="todo id"),
):
    delete_todo_id = await _delete_todo(todo_id=todo_id)
    if delete_todo_id is not None:

        url = user_router.url_path_for("home")
        return RedirectResponse(url=url, status_code=HTTP_302_FOUND)
    else:
        raise HTTPException(
            status_code=404, detail=f"Todo with id {todo_id} not found."
        )
