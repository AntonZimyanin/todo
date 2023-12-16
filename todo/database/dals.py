from typing import Union

from sqlalchemy import select, delete, update
from sqlalchemy.orm.session import Session

from todo.database.models import Todo, User
from todo.api.schemas import EmptyList


class TodoDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def create_todo(
        self,
        title,
        user_id
    ) -> Todo:
        new_todo = Todo(title=title, user_id=user_id)
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
        todo_row = res.fetchone()
        if todo_row is not None:
            return todo_row[0]

    def update_todo(self, todo_id: int, **kwargs) -> Union[int, None]:
        query = update(Todo).where(Todo.id == todo_id).values(kwargs).returning(Todo.id)
        res = self.db_session.execute(query)
        update_todo_row = res.fetchone()
        if update_todo_row is not None:
            return update_todo_row[0]

    def select_all(self, user_id: int) -> Union[list, EmptyList]:
        query = select(Todo).where(Todo.user_id == user_id)
        res = self.db_session.execute(query)
        todo_tuple_list = res.fetchall()

        if todo_tuple_list == []:
            return []

        todo_list = [todo for todo_tuple in todo_tuple_list for todo in todo_tuple]

        return todo_list



class UserDal:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session


    def create_user(
            self, 
            name
    ) -> User:
        new_user = User(name=name)
        self.db_session.add(new_user)
        self.db_session.flush()

        return new_user


    def select_all(self): 
        query = select(User)
        user_tuple_list = self.db_session.execute(query).fetchall()
        
        if user_tuple_list is None: 
            return  
        
        user_list = [user for user_tuple in user_tuple_list for user in user_tuple]

        return user_list
        
    
    def delete_user(self, user_id: int) -> Union[int, None]:
        pass


    def get_user_by_name(self, name: str) -> Union[int, None]: 
        query = select(User).where(User.name == name)
        res = self.db_session.execute(query)
        user_row = res.fetchone()
        
        if user_row is not None: 
            return user_row[0]

    def get_user_by_id(self, id: int) -> Union[User, None]:
        query = select(User).where(User.id == id)
        res = self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]


    def update_user(self, user_id: int, **kwargs) -> Union[int, None]: 
        pass        





    