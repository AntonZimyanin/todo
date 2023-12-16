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
from todo.api.action.user import (
    _create_user, 
    _get_user_by_id, 
    _get_user_by_name,
    _select_all_user
)
from todo.admin_data import admin_data_dict
from todo.admin_data import admin_field_name


auth_router = APIRouter(prefix="/auth", tags=["auth"])
todo_router = APIRouter(prefix="/todo", tags=["todo"])


templates = Jinja2Templates(directory="todo/templates")

##########################
#   TODO_
#########################


@todo_router.get("/home/{user_id}", response_class=HTMLResponse)
async def home(request: Request, user_id: int, db_session: Session = Depends(get_db)):
    todo_list = _select_all_todo(user_id=user_id, session=db_session)
    user = _get_user_by_id(id=user_id, session=db_session)

    return templates.TemplateResponse(
        "todo/index.html",
        {
            "request": request,
            "app_name": config.app_name,
            "todo_list": todo_list,
            "user": user
        },
    )


@todo_router.post("/add", response_class=RedirectResponse)
async def add(
    title: Annotated[str | None, Form(min_length=1)] = None,
    user_id: Annotated[str | None, Form(...)] = None,
    db_session: Session = Depends(get_db),
):
    if user_id is not None:
        _create_todo(title=title, user_id=user_id, session=db_session)
        url = todo_router.url_path_for("home", user_id=user_id)
        return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
    


@todo_router.get("/update/{todo_id}/{is_complete}/{user_id}", response_class=RedirectResponse)
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
        url = todo_router.url_path_for("home", user_id=user_id)
        return RedirectResponse(url=url, status_code=HTTP_302_FOUND)
    else:
        raise HTTPException(
            status_code=404, detail=f"Todo with id {todo_id} not found."
        )


@todo_router.get("/delete/{todo_id}/{user_id}", response_class=RedirectResponse)
async def delete(
    todo_id: int = Path(..., description="todo id"),
    user_id: int = Path(..., description="user id"),
    db_session: Session = Depends(get_db),
):
    delete_todo_id = _delete_todo(todo_id=todo_id, session=db_session)
    if delete_todo_id is not None:

        url = todo_router.url_path_for("home", user_id=user_id)
        return RedirectResponse(url=url, status_code=HTTP_302_FOUND)
    else:
        raise HTTPException(
            status_code=404, detail=f"Todo with id {todo_id} not found."
        )


########################
#   AUTH
########################


@auth_router.get("/", response_class=HTMLResponse)
async def get_init_page(request: Request):

    return templates.TemplateResponse(
        "todo/log_in.html",
        {
            "request": request,
            "app_name": config.app_name
        },
    )


@auth_router.post("/log_in", response_class=RedirectResponse)
async def log_in(
    name: Annotated[str | None, Form(min_length=1)] = None,
    db_session: Session = Depends(get_db),
):
    user = _get_user_by_name(name=name,session=db_session)
    if name == admin_field_name: 
        url = auth_router.url_path_for("log_in_admin_page")
        return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
    
    if user is not None: 
        url = todo_router.url_path_for("home", user_id=user.id)
        return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
    else: 
        pass


@auth_router.get("/sign_up/page", response_class=HTMLResponse)
async def get_sign_up_page(request: Request):

    return templates.TemplateResponse(
        "todo/sign_up.html",
        {
            "request": request,
            "app_name": config.app_name
        },
    )


@auth_router.post("/sign_up", response_class=HTMLResponse)
async def sign_up(
    name: Annotated[str | None, Form(min_length=1)] = None,
    db_session: Session = Depends(get_db),
): 
    user = _get_user_by_name(name=name, session=db_session)
    if user is None: 
        user = _create_user(name=name, session=db_session)
        # url = todo_router.url_path_for("home", user_name=user.name)

        url = todo_router.url_path_for("home", user_id=user.id)
        return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
    else: 
        #user существует
        pass


@auth_router.get("/admin/log_in", response_class=HTMLResponse)
async def log_in_admin_page(request: Request):

    return templates.TemplateResponse(
        "todo/log_in_admin.html",
        {
            "request": request,
            "app_name": config.app_name
        },  
    )   


@auth_router.post("/admin/log_in/request", response_class=RedirectResponse)
async def log_in_admin(
    password: Annotated[str | None, Form(min_length=1)] = None,
    db_session: Session = Depends(get_db),
):

    if password == admin_data_dict[admin_field_name]:   
        user = _get_user_by_name(name=admin_field_name, session=db_session)
        url = todo_router.url_path_for("home", user_id=user.id)
        return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
    else: 
        url = auth_router.url_path_for("incorrect_password")
        return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
    

@auth_router.post("/log_out", response_class=HTMLResponse)
async def log_out():
    url = auth_router.url_path_for("get_init_page")
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


#####################
#   ADMIN
######################

admin_router = APIRouter(prefix="/admin", tags=["admin"])


@admin_router.get("/incorrect_password/", response_class=HTMLResponse)
async def incorrect_password(request: Request):

    return templates.TemplateResponse(
        "todo/log_in_admin_incorrect.html",
        {
            "request": request,
            "app_name": config.app_name
        },
    )


##########################
#   PROFILE
##########################


profile_router = APIRouter(prefix="/profile", tags=["profile"])


@profile_router.get("/{user_id}", response_class=HTMLResponse)
async def profile_page(request: Request, user_id: int, db_session: Session = Depends(get_db)):
    todo_list = _select_all_todo(user_id=user_id, session=db_session)
    user = _get_user_by_id(id=user_id, session=db_session)

    return templates.TemplateResponse(
        "todo/profile.html",
        {
            "request": request,
            "app_name": config.app_name,
            "todo_list": todo_list,
            "user": user,
        },
    )


@profile_router.get("/admin_button/get/{user_id}", response_class=RedirectResponse)
async def profile_admin_request(
    user_id: int = Path(..., description="user name"),
    db_session: Session = Depends(get_db),
):
    user = _get_user_by_id(id=user_id, session=db_session)
    url = profile_router.url_path_for("profile_admin_page", user_id=user.id)
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@profile_router.get("/admin/{user_id}", response_class=HTMLResponse)
async def profile_admin_page(request: Request, user_id: int, db_session: Session = Depends(get_db)):
    todo_list = _select_all_todo(user_id=user_id, session=db_session)
    user = _get_user_by_id(id=user_id, session=db_session)
    user_list = _select_all_user(session=db_session)

    return templates.TemplateResponse(
        "todo/admin_profile.html",
        {
            "request": request,
            "app_name": config.app_name,
            "todo_list": todo_list,
            "user": user,
            "user_list": user_list
        },
    )

