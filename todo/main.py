from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()


app.mount("/static", StaticFiles(directory="todo/static"), name="static")
templates = Jinja2Templates(directory="todo/templates")


from todo.routes import home
