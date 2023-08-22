from tortoise.models import Model
from tortoise import fields


class Todo(Model):
    id = fields.IntField(pk=True)
    title = fields.TextField()
    is_complete = fields.BooleanField(default=False)
