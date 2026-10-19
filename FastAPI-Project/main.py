from  fastapi import FastAPI
from src.utils.db import Base, engine
from src.tasks.models import TaskModel
from src.tasks.router import task_router

Base.metadata.create_all(engine)

app = FastAPI(title='This is my task Management Application')
app.include_router(task_router)

