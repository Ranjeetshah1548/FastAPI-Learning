from fastapi import APIRouter,Depends
from src.tasks import controller
from src.tasks.dtos import TaskSchema
from src.utils.db import get_db

# create a router app
task_router = APIRouter(prefix="/tasks")

## create a route for post a task
@task_router.post("/create")
def create_task(body: TaskSchema, db = Depends(get_db)):
    return controller.create_task(body, db)

## create a route for get all task
@task_router.get("/all_tasks")
def get_all_task(db = Depends(get_db)):
    return controller.get_task(db)

## create a route for get one task.
@task_router.get("/one_task/{task_id}")
def get_one_task(task_id:int, db = Depends(get_db)):
    return controller.get_one_task(task_id, db)