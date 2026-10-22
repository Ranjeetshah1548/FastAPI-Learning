from fastapi import APIRouter,Depends, status
from src.tasks import controller
from src.tasks.dtos import TaskSchema
from src.utils.db import get_db

# create a router app
task_router = APIRouter(prefix="/tasks")

## create a route for post a task
@task_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_task(body: TaskSchema, db = Depends(get_db)):
    return controller.create_task(body, db)

## create a route for get all task
@task_router.get("/all_tasks", status_code=status.HTTP_200_OK)
def get_all_task(db = Depends(get_db)):
    return controller.get_task(db)

## create a route for get one task.
@task_router.get("/one_task/{task_id}" , status_code=status.HTTP_200_OK)
def get_one_task(task_id:int, db = Depends(get_db)):
    return controller.get_one_task(task_id, db)

## create a route for update a task.
@task_router.put("/update_task/{task_id}", status_code=status.HTTP_201_CREATED)
def update_task(body:TaskSchema, task_id:int, db=Depends(get_db)):
    return controller.update_task(body, task_id, db)

## create a route for delete a task.
@task_router.delete("/delete_task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id:int, db=Depends(get_db)):
    return controller.delete_task(task_id,db)

