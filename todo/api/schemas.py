from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class CreateTodo(BaseModel):
    title: str
    is_complete: bool = False


class ShowTodo(TunedModel):
    id: int
    title: str
    is_complete: bool


class EmptyList: 
    pass
