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
