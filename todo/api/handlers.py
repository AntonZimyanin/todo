from typing import Annotated

from fastapi import Request, Depends, Form, APIRouter, Path
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_303_SEE_OTHER, HTTP_302_FOUND
from sqlalchemy.orm import Session

from todo.database.base import get_db
from todo.config import config
from todo.api.action.todo import (
    _select_all_todo,
    _create_todo,
    _update_todo,
    _delete_todo,
)

user_router = APIRouter()

templates = Jinja2Templates(directory="todo/templates")


@user_router.get("/", response_class=HTMLResponse)
async def home(request: Request, session: Session = Depends(get_db)):
    todo_list = _select_all_todo(session=session)

    return templates.TemplateResponse(
        "todo/index.html",
        {
            "request": request,
            "app_name": config.app_name,
            "todo_list": todo_list,
            "is_title": True,
        },
    )


@user_router.get("/nullable_title", response_class=HTMLResponse)
async def nullable_title(request: Request, session: Session = Depends(get_db)):
    todos = _select_all_todo(session=session)
    return templates.TemplateResponse(
        "todo/index.html",
        {
            "request": request,
            "app_name": config.app_name,
            "todo_list": todos,
            "is_title": False,
        },
    )


@user_router.post("/add", response_class=RedirectResponse)
async def add(
    title: Annotated[str | None, Form(min_length=1)] = None,
    db_session: Session = Depends(get_db),
):
    if title is not None:
        _create_todo(title=title, session=db_session)
        url = user_router.url_path_for("home")
        return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
    else:
        url = user_router.url_path_for("nullable_title")
        return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@user_router.get("/update/{todo_id}/{is_complete}", response_class=RedirectResponse)
async def update(
    todo_id: int = Path(..., description="todo id"),
    is_complete: bool = Path(..., description="state todo"),
    db_session: Session = Depends(get_db),
):
    update_todo_id = _update_todo(
        todo_id=todo_id, session=db_session, params={"is_complete": is_complete}
    )
    if update_todo_id is not None:
        url = user_router.url_path_for("home")
        return RedirectResponse(url=url, status_code=HTTP_302_FOUND)
    else:
        raise HTTPException(
            status_code=404, detail=f"Todo with id {todo_id} not found."
        )


@user_router.get("/delete/{todo_id}", response_class=RedirectResponse)
async def delete(
    todo_id: int = Path(..., description="todo id"),
    db_session: Session = Depends(get_db),
):
    delete_todo_id = _delete_todo(todo_id=todo_id, session=db_session)
    if delete_todo_id is not None:

        url = user_router.url_path_for("home")
        return RedirectResponse(url=url, status_code=HTTP_302_FOUND)
    else:
        raise HTTPException(
            status_code=404, detail=f"Todo with id {todo_id} not found."
        )
