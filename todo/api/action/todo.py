from typing import Union

from sqlalchemy.orm.session import Session

from todo.api.schemas import CreateTodo, ShowTodo, EmptyList
from todo.database.dals import TodoDAL
from todo.database.models import Todo

# def _create_todo(body: CreateTodo, session: Session):
def _create_todo(title: str, user_id: int, session: Session) -> ShowTodo:
    with session.begin():
        todo_dal = TodoDAL(session)
        todo = todo_dal.create_todo(title=title, user_id=user_id)

        return ShowTodo(id=todo.id, title=todo.title, is_complete=todo.is_complete)


def _delete_todo(todo_id, session: Session) -> Union[int, None]:
    with session.begin():
        todo_dal = TodoDAL(session)
        deleted_todo_id = todo_dal.delete_todo(todo_id=todo_id)

        return deleted_todo_id


def _update_todo(todo_id, session: Session, params: dict) -> Union[int, None]:
    with session.begin():
        todo_dal = TodoDAL(session)
        update_todo_id = todo_dal.update_todo(todo_id=todo_id, **params)

        return update_todo_id


def _get_todo_by_id(todo_id: int, session: Session) -> Union[Todo, None]:
    with session.begin():
        todo_dal = TodoDAL(session)
        todo = todo_dal.get_todo_by_id(todo_id=todo_id)

        if todo is not None:
            return todo


def _select_all_todo(user_id: int, session: Session) -> Union[list, EmptyList]:
    with session.begin():
        todo_dal = TodoDAL(session)
        todos = todo_dal.select_all(user_id=user_id)

        if todos is not None:
            return todos
        
    # todo_dal = TodoDAL(session)
    # todos = todo_dal.select_all(user_id=user_id)

    # if todos is not None:
    #     return todos