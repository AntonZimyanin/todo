from typing import Union

from sqlalchemy import select, delete, update
from sqlalchemy.orm.session import Session

from todo.database.models import Todo
from todo.api.schemas import EmptyList


class TodoDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def create_todo(
        self,
        title,
    ) -> Todo:
        new_todo = Todo(title=title)
        self.db_session.add(new_todo)
        self.db_session.flush()

        return new_todo

    def delete_todo(self, todo_id: int) -> Union[int, None]:
        query = delete(Todo).where(Todo.id == todo_id).returning(Todo.id)
        res = self.db_session.execute(query)
        deleted_todo_id_row = res.fetchone()
        if deleted_todo_id_row is not None:
            return deleted_todo_id_row[0]

    def get_todo_by_id(self, todo_id: int) -> Union[Todo, None]:
        query = select(Todo).where(Todo.id == todo_id)
        res = self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    def update_todo(self, todo_id: int, **kwargs) -> Union[int, None]:
        query = update(Todo).where(Todo.id == todo_id).values(kwargs).returning(Todo.id)
        res = self.db_session.execute(query)
        update_todo_row = res.fetchone()
        if update_todo_row is not None:
            return update_todo_row[0]

    def select_all(self) -> Union[list, EmptyList]:
        query = select(Todo)
        res = self.db_session.execute(query)
        todo_tuple_list = res.fetchall()

        if todo_tuple_list == []:
            return []

        todo_list = [todo for todo_tuple in todo_tuple_list for todo in todo_tuple]

        return todo_list
