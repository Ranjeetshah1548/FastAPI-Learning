from fastapi import FastAPI, Path, Query, HTTPException
import json

app = FastAPI()


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