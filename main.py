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
    



# Path Parameters
@app.get("/students/{student_id}")
def student_info(student_id: int):
    # If student exists, return the student; otherwise return error
    for s in students:
        if s.get("id") == student_id:
            return s

    return {
        "error": "Student Id not found.."
    }


# Query Parameters
@app.get("/greet")
def greet_user(name: str, age: int):
    return {
        "greet": f"Hello {name}, Your age is {age}"
    }


# Multiple Query Parameters
@app.get("/greets")
def user_greet(request: Request):
    query_param = dict(request.query_params)

    return {
        "Greet": f"Hello {query_param.get('name')}, Your age is {query_param.get('age')}"
    }

## Deferent types of HTTS Methos

## import pydentic bashmodel
from pydantic import BaseModel
class studentDTO(BaseModel):
    id:int
    name:str
    Class:str

## Create a Post Routes
@app.post("/create_student")
def create_student(create_student:studentDTO):
    create_student = create_student.model_dump()
    students.append(create_student)

    return{"status":"Student Created Successfully..","Students":students}


## Create a Put Routes
@app.put("/update_student/{id}")
def update_student(update_student:studentDTO, id:int):

    for index, onestudent in enumerate(students):
        if onestudent.get("id") == id:
            print(index,onestudent)
            students[index] = update_student.model_dump()
            return{"status":"Student Updated Successfully..","Student":update_student}


    return {
            "error": "Student Id not found.."
        }


## create a delete Routes
@app.delete("/delete_student/{id}")
def delete_student(id:int):

    for index, onestudent in enumerate(students):
        if onestudent.get("id") == id:
            delete_student = students.pop(index)

            return{"status":"Student Deleted Successfully..","Student":delete_student}

    return {
                "error": "Student Id not found.."
            }

