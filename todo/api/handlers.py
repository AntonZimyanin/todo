from typing import Annotated

from fastapi import Request, Depends, Form, APIRouter, Path
from fastapi import Body
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
from todo.api.action.user import (
    _create_user, 
    _update_user, 
    _get_user_by_id, 
    _get_user_by_name,
    _select_user
)

user_router = APIRouter()

templates = Jinja2Templates(directory="todo/templates")


@user_router.get("/home/{user_id}", response_class=HTMLResponse)
async def home(request: Request, user_id: int, db_session: Session = Depends(get_db)):
    todo_list = _select_all_todo(user_id=user_id, session=db_session)
    user = _get_user_by_id(id=user_id, session=db_session)

    return templates.TemplateResponse(
        "todo/index.html",
        {
            "request": request,
            "app_name": config.app_name,
            "todo_list": todo_list,
            "is_title": True,
            "user": user
        },
    )


@user_router.post("/log_out", response_class=HTMLResponse)
async def log_out():
    url = user_router.url_path_for("get_init_page")
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@user_router.post("/sign_up", response_class=HTMLResponse)
async def sign_up(
    name: Annotated[str | None, Form(min_length=1)] = None,
    db_session: Session = Depends(get_db),
): 
    user = _get_user_by_name(name=name, session=db_session)
    if user is None: 
        user = _create_user(name=name, session=db_session)
        # url = user_router.url_path_for("home", user_name=user.name)

        url = user_router.url_path_for("home", user_id=user.id)
        return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
    else: 
        #user существует
        pass


# @user_router.get("/sign_up", response_class=HTMLResponse)
# async def sign_up(
#     request: Request, 
#     name: Annotated[str | None, Form(min_length=1)] = None,
#     db_session: Session = Depends(get_db),
# ): 
#     user = _get_user_by_name(name=name, session=db_session)
#     todo_list = _select_all_todo(session=db_session)

#     if user is None: 
#         _create_user(name=name, session=db_session)

#         return templates.TemplateResponse(
#         "todo/index.html",  
#         {
#             "request": request,
#             "app_name": config.app_name,
#             "todo_list": todo_list,
#             "is_title": True,
#             "user": user
#         },
#     )

#         url = user_router.url_path_for("home")
#         return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
#     else: 
#         #user существует
#         pass

# @user_router.post("/sign_up", response_class=HTMLResponse)
# async def sign_up(
#     name: Annotated[str | None, Form(min_length=1)] = None,
#     db_session: Session = Depends(get_db),
# ): 
#     user = _get_user_by_name(name=name, session=db_session)
#     if user is None: 
#         _create_user(name=name, session=db_session)
#         url = user_router.url_path_for("home")
#         return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
#     else: 
#         #user существует
#         pass


@user_router.get("/sign_up_page", response_class=HTMLResponse)
async def get_sign_up_page(request: Request):

    return templates.TemplateResponse(
        "todo/sign_up.html",
        {
            "request": request,
            "app_name": config.app_name
        },
    )


# @user_router.post("/user_add", response_class=RedirectResponse)
# async def user_add(
#     name: Annotated[str | None, Form(min_length=1)] = None,
#     db_session: Session = Depends(get_db),
# ):
#     if name is not None: 
#         _create_user(name=name, session=db_session)
#         url = user_router.url_path_for("home")
#         return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
#     else: 
#         url = user_router.url_path_for("nullable_name")
#         return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@user_router.get("/", response_class=HTMLResponse)
async def get_init_page(request: Request):

    return templates.TemplateResponse(
        "todo/log_in.html",
        {
            "request": request,
            "app_name": config.app_name
        },
    )


@user_router.post("/log_in", response_class=RedirectResponse)
async def log_in(
    name: Annotated[str | None, Form(min_length=1)] = None,
    db_session: Session = Depends(get_db),
):
    user = _get_user_by_name(name=name,session=db_session)
    if user is not None: 
        url = user_router.url_path_for("home", user_id=user.id)
        return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
    else: 
        pass
        # url = user_router.url_path_for("home")

        # return RedirectResponse(url=url, status_code=304)


@user_router.get("/nullable_name", response_class=HTMLResponse)
async def nullable_name(request: Request, session: Session = Depends(get_db)):
    pass


@user_router.get("/nullable_title", response_class=HTMLResponse)
async def nullable_title(request: Request, user_id: int, session: Session = Depends(get_db)):
    todos = _select_all_todo(session=session)
    user = _get_user_by_id(id=user_id)

    return templates.TemplateResponse(
        "todo/index.html",
        {
            "request": request,
            "app_name": config.app_name,
            "todo_list": todos,
            "is_title": False,
            "user": user
        },
    )


@user_router.post("/add", response_class=RedirectResponse)
async def add(
    title: Annotated[str | None, Form(min_length=1)] = None,
    user_id: Annotated[str | None, Form(...)] = None,
    db_session: Session = Depends(get_db),
):
    if title is not None and user_id is not None:
        _create_todo(title=title, user_id=user_id, session=db_session)
        url = user_router.url_path_for("home", user_id=user_id)
        return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
    else:
        url = user_router.url_path_for("nullable_title", user_id=user_id)
        return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@user_router.get("/update/{todo_id}/{is_complete}/{user_id}", response_class=RedirectResponse)
async def update(
    todo_id: int = Path(..., description="todo id"),
    is_complete: bool = Path(..., description="state todo"),
    user_id: int = Path(..., description="user id"),
    db_session: Session = Depends(get_db),
):
    update_todo_id = _update_todo(
        todo_id=todo_id, session=db_session, params={"is_complete": is_complete}
    )
    
    if update_todo_id is not None:
        url = user_router.url_path_for("home", user_id=user_id)
        return RedirectResponse(url=url, status_code=HTTP_302_FOUND)
    else:
        raise HTTPException(
            status_code=404, detail=f"Todo with id {todo_id} not found."
        )


@user_router.get("/delete/{todo_id}/{user_id}", response_class=RedirectResponse)
async def delete(
    todo_id: int = Path(..., description="todo id"),
    user_id: int = Path(..., description="user id"),
    db_session: Session = Depends(get_db),
):
    delete_todo_id = _delete_todo(todo_id=todo_id, session=db_session)
    if delete_todo_id is not None:

        url = user_router.url_path_for("home", user_id=user_id)
        return RedirectResponse(url=url, status_code=HTTP_302_FOUND)
    else:
        raise HTTPException(
            status_code=404, detail=f"Todo with id {todo_id} not found."
        )


@user_router.get("/profile/{user_id}", response_class=HTMLResponse)
async def profile_page(request: Request, user_id: int, db_session: Session = Depends(get_db)):
    todo_list = _select_all_todo(user_id=user_id, session=db_session)
    user = _get_user_by_id(id=user_id, session=db_session)

    return templates.TemplateResponse(
        "todo/profile.html",
        {
            "request": request,
            "app_name": config.app_name,
            "todo_list": todo_list,
            "is_title": True,
            "user": user
        },
    )
