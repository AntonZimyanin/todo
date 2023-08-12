from typing import Annotated

from fastapi import Request, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_302_FOUND
from sqlalchemy.orm import Session

from todo.main import app, templates
from todo.database.base import get_db
from todo.database.models import Todo
from todo.config import config


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, session: Session = Depends(get_db)):
    todos = session.query(Todo).all()
    return templates.TemplateResponse(
        "todo/index.html",
        {
            "request": request,
            "app_name": config.app_name.get_secret_value(),
            "todo_list": todos,
            "is_title": True,
        },
    )


@app.get("/blank_title", response_class=HTMLResponse)
async def nullable_title(request: Request, session: Session = Depends(get_db)):
    todos = session.query(Todo).all()
    return templates.TemplateResponse(
        "todo/index.html",
        {
            "request": request,
            "app_name": config.app_name.get_secret_value(),
            "todo_list": todos,
            "is_title": False,
        },
    )


@app.post("/add", response_class=RedirectResponse)
async def add(
    title: Annotated[str | None, Form(min_length=1)] = None,
    db_session: Session = Depends(get_db),
):
    if title is not None:
        new_todo = Todo(title=title)
        db_session.add(new_todo)
        db_session.commit()

        url = app.url_path_for("home")
        return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
    else:
        url = app.url_path_for("nullable_title")
        return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@app.get("/update/{todo_id}", response_class=RedirectResponse)
async def update(todo_id: int, db_session: Session = Depends(get_db)):
    todo = db_session.query(Todo).filter(Todo.id == todo_id).first()
    todo.is_complete = not todo.is_complete
    db_session.commit()

    url = app.url_path_for("home")

    return RedirectResponse(url=url, status_code=HTTP_302_FOUND)


@app.get("/delete/{todo_id}", response_class=RedirectResponse)
async def delete(todo_id: int, db_session: Session = Depends(get_db)):
    todo = db_session.query(Todo).filter_by(id=todo_id).first()
    db_session.delete(todo)
    db_session.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=HTTP_302_FOUND)
