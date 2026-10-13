from fastapi import FastAPI,Request
from data import students

app = FastAPI()
## multi route 
@app.get("/")
def home():
    return "hello FastAPI"

@app.get("/contact")
def contact():
    return "Thanks for contacting us!"

@app.get("/about")
def about():
    return "This is all about us.."

@app.get("/student")
def get_student():
    return students
    
## path params.
@app.get("/students/{student_id}")
def student_info(student_id : int ):
    ## if student present with id then return otherwise return erro
    for s in students:
        if s.get("id")==student_id:
           return s

    return {
        "error":"Student Id not found.."
    }


## query params
@app.get("/greet")
def greet_user(name:str,age:int):
    return {
        "greet": f"Hello {name},Your age is {age} "
    }
        
## N number of params
@app.get("/greets")
def user_greet(request:Request):
    query_param = dict(request.query_params)

    return {
        "Greet": f"Hello {query_param.get("name")}, Your age is {query_param.get("age")}"
    }



