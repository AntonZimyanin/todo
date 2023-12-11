from typing import Union

from sqlalchemy.orm.session import Session

from todo.database.dals import UserDal
from todo.database.models import User
from todo.api.schemas import CreateUser, ShowUser


def _create_user(name: str, session: Session) -> ShowUser:
    with session.begin():   
        user_dal = UserDal(session)
        user = user_dal.create_user(name=name)

        return user
    


def _get_user_by_id(id: int, session: Session) -> ShowUser: 
    with session.begin():   
        user_dal = UserDal(session)
        user = user_dal.get_user_by_id(id=id)

        if user is not None:
            return user
        

def _get_user_by_name(name: str, session: Session) -> ShowUser: 
    with session.begin():   
        user_dal = UserDal(session)
        user = user_dal.get_user_by_name(name=name)

        if user is not None:
            return user


def _update_user(user_id, session: Session, params: dict) -> Union[int, None]:
    with session.begin():
        user_dal = UserDal(session)
        update_user_id = user_dal.update_user(user_id=user_id, **params)

        return update_user_id
    

def _select_user(session: Session) -> Union[User, None]: 
    with session.begin():
        user_dal = UserDal(session)
        user = user_dal.select_user()

        if user is not None: 
            return user