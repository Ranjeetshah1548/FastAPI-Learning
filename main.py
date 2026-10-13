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
    

