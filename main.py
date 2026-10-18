from fastapi import FastAPI, Path, Query, HTTPException 
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal,Optional
import json

app = FastAPI()

## Create a patient pydentic model for data validation
class patient (BaseModel):
    id: Annotated[str, Field(..., description='Id of the patient', examples=['P001'])]
    name : Annotated[str, Field(..., description='Name of Patient')]
    city:Annotated[str, Field(..., description='City where the patient is living')]
    age:Annotated[int, Field(..., gt=0, lt=120, description='age of patient')]
    gender:Annotated[Literal['male','female','other'],Field(..., description='gender of patient ')]
    height:Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight:Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]
    
    ## create a computed field for bmi
    @computed_field
    @property
    def bmi (self)-> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    ## create a computed field for verdict
    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 30 :
            return 'Normal'
        else:
            return 'Obese'





@app.get("/")
def greet():
    return {'massage': 'Patients Management System'}


@app.get("/about")
def about():
    return{'massage':'A fully Functional API to manage Your Patients Records'}


## Helper Fuction to Load data

def load_data():
    with open('patients_data.json','r') as f:
         data = json.load(f)
    return data

##Helper function to save data into json file 
def save_data(data):
    with open('patients_data.json', 'w' ) as f:
        json.dump(data, f)


## Routes for View Patients Data
@app.get("/view")
def view():
    data = load_data()
    return data

## Path Params with using path()Function and HttpException
@app.get("/patient/{patient_id}")
def view_patient(patient_id:str = Path(..., description='ID of the patient in the DB',example='P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException (status_code=404, detail='patient not fount')

## Query params 
@app.get('/sort')
def sort_patients(sort_by:str=Query(description='Sort on the basis of Height, Weight, or bmi'),order:str = Query('asc', description='sort in asc or dsc order')):

    valied_fields = ['height','weight','bmi']

    if sort_by not in valied_fields:
        raise HTTPException (status_code=400, detail=f'Invalid field from {valied_fields}')

    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Invalid order select between asc and desc')

    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by,0), reverse=sort_order)

    return sorted_data

## create a route for create a patient
@app.post("/create")
def create_patient(patient : patient):

    #load existing data
    data = load_data()

    #check if the patient already exist
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exist')

    #new patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    #save into the json file 
    save_data(data)

    return JSONResponse(status_code=201, content='patient Created Successfully')


