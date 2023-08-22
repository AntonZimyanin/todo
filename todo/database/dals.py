from typing import Union

from todo.database.models import Todo
from todo.api.schemas import EmptyList


class TodoDAL:
    """Data Access Layer for operating user info"""

    def __init__(
        self,
    ) -> None:
        pass

    async def create_todo(
        self,
        title,
    ) -> Todo:
        new_todo = await Todo.create(title=title)
        return new_todo

    async def delete_todo(self, todo_id: int) -> Union[int, None]:
        deleted_todo = await Todo.filter(id=todo_id).delete()
        if deleted_todo:
            return todo_id

    async def get_todo_by_id(self, todo_id: int) -> Union[Todo, None]:
        todo = await Todo.get_or_none(id=todo_id)
        return todo

    async def update_todo(self, todo_id: int, **kwargs) -> Union[Todo, None]:
        """
        Update a Todo item with the specified ID using the provided keyword arguments.

        This function updates the attributes of a Todo item in the database with the given ID.
        The attributes to update are provided as keyword arguments.

        Parameters:
        - todo_id (int): The unique identifier of the Todo item to be updated.
        - **kwargs: Keyword arguments representing the attributes to update in the Todo item.
                    The keyword should match the attribute name in the Todo class.

        Returns:
        - Union[Todo, None]: If the update is successful, returns the updated Todo item.
                            If no matching Todo item is found, returns None.
        """
        update_todo = await Todo.get_or_none(id=todo_id)
        if update_todo is not None:
            update_todo.update_from_dict(kwargs)
            await update_todo.save()

            return update_todo

    async def select_all(self) -> Union[list, EmptyList]:
        todos = await Todo.all()

        if todos == []:
            return []

        return todos
