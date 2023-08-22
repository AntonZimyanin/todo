from typing import Union

from todo.api.schemas import EmptyList
from todo.database.models import Todo
from todo.database.dals import TodoDAL


async def _create_todo(title: str) -> Todo:
    todo_dal = TodoDAL()
    new_todo = await todo_dal.create_todo(title=title)

    return new_todo


async def _delete_todo(todo_id: int) -> Union[int, None]:
    todo_dal = TodoDAL()
    delete_todo_id = await todo_dal.delete_todo(todo_id=todo_id)

    return delete_todo_id


async def _update_todo(todo_id: int, params: dict) -> Union[int, None]:
    todo_dal = TodoDAL()
    update_todo = await todo_dal.update_todo(todo_id=todo_id, **params)

    return update_todo


async def _get_todo_by_id(todo_id: int) -> Union[Todo, None]:
    todo_dal = TodoDAL()
    todo = await todo_dal.get_todo_by_id(todo_id=todo_id)

    return todo


async def _select_all_todo() -> Union[list, EmptyList]:
    todo_dal = TodoDAL()
    todos = await todo_dal.select_all()

    return todos
