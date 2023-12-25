from typing import List

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, backref
from sqlalchemy.orm import mapped_column, relationship

from todo.database.base import Base
from todo.database.base import engine


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(), nullable=False)
    is_complete: Mapped[bool]= mapped_column(Boolean, default=False)


    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="todos")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))

    # todos: Mapped[List["Todo"]] = relationship(back_populates="user", backref=backref("user", cascade="all,delete"))
    todos: Mapped[List["Todo"]] = relationship(back_populates="user")


Base.metadata.create_all(engine)
