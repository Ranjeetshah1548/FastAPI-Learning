from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException


## controller for create  a task 
def create_task(body, db):
    data = body.model_dump()
    new_task = TaskModel(title= data['title'],
                         description= data['description'], 
                         is_completed= data ['is_completed'] 
                         )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return {"status":"Task Created Successfully...","data":new_task}


## controller for get all tasks
def get_task(db:Session):
    tasks = db.query(TaskModel).all()
    return {"ststus":"All Tasks", "data": tasks}

## controller for get one task
def get_one_task(task_id:int, db:Session):
    one_task = db.query(TaskModel).get(task_id)

    if not one_task:
        raise HTTPException(status_code=404, detail='Task it not found!!')

    return {"ststus": "Task Fatched Successfully...","data":one_task}

## controller for update task.
def update_task(body:TaskSchema ,task_id:int, db:Session):

    one_task = db.query(TaskModel).get(task_id)
    
    if not one_task:
        raise HTTPException(status_code=404, detail='Task it not found!!')
    
#  -> for all fields
#   one_task.title = body.title
#   one_task.description = body.description
#   one_task.is_completed = body.is_completed

# -> for only selective  field
    body = body.model_dump()
    for field, value in body.items():
        setattr(one_task, field, value)

    db.add(one_task)
    db.commit()
    db.refresh(one_task)

    return {"ststus": "Task Updated Successfully...","data":one_task}
                

## controller for delete task.
def delete_task(task_id:int, db:Session):
    one_task = db.query(TaskModel).get(task_id)

    if not one_task:
            raise HTTPException(status_code=404, detail='Task it not found!!')

    db.delete(one_task)
    db.commit()


    return {"ststus": "Task Deleted Successfully..."}


