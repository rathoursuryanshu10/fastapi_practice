from http.client import HTTPResponse

from fastapi import FastAPI, HTTPException,Path, Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str,Field(...,description="ID of Patient",example="P001")]
    name: Annotated[str,Field(...,description="Name of Patient",example="John Doe")]
    city: Annotated[str,Field(...,description="City of Patient",example="New York")]
    age: Annotated[int,Field(...,gt=0,lt=120,description="Age of Patient",example=30)]
    gender: Annotated[Literal["Male","Female","Other"],Field(...,description="Gender of Patient",example="Male")]
    height: Annotated[float,Field(...,gt=0,description="Height of Patient in meters",example=1.65)]
    weight: Annotated[float,Field(...,gt=0,description="Weight of Patient in kg",example=58.0)]
    @computed_field()
    @property
    def bmi(self)->float:
        bmi_value = round(self.weight / (self.height ** 2),2)
        return bmi_value
    @computed_field()
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal weight"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obesity"

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str],Field(default=None)]
    city: Annotated[Optional[str],Field(default=None)]
    age: Annotated[Optional[int],Field(default=None)]
    gender: Annotated[Optional[Literal["Male","Female","Other"]],Field(default=None)] 
    height: Annotated[Optional[float],Field(default=None,gt=0)]
    weight: Annotated[Optional[float],Field(default=None,gt=0)]

def load_data():
    with open("patients.json", "r") as f:
        return json.load(f)
def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)

@app.get('/')
def hello():
    return {"message": "Patients management system API is up and running!"}

@app.get('/about')
def about():
    return {"message": "A fully-featured patients management system API."}

@app.get('/view')
def view_patients():
    data = load_data()
    return data

# path parameter example: /patient/P001
@app.get('/patient/{patient_id}')
def view_patient(patient_id:str = Path(...,description="The ID of the patient to retrieve",examples="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found.")

# query parameter example: /search?city=New%20York
@app.get('/sort')
def sort(sort_by:str=Query(...,description="The field to sort patients by height, weight,age or bmi"),order:str=Query("asc",description="The order to sort asc,desc"),example="age"):
    valid_sort_fields = ["height", "weight", "bmi", "age"]
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}. Valid fields are height, weight, age, bmi.")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail=f"Invalid order: {order}. Valid orders are asc or desc.")
    data = load_data()
    sort_order = True if order == "desc" else False
    sorted_patients = sorted(data.values(), key=lambda item: item.get(sort_by,0),reverse = sort_order)
    return sorted_patients

@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail=f"Patient with ID {patient.id} already exists.")
    data[patient.id] = patient.model_dump(exclude={'id'})
    save_data(data)
    return JSONResponse(status_code=201, content={"message": f"Patient with ID {patient.id} created successfully."})

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found.")
    existing_patient = data[patient_id]
    update_data = patient_update.model_dump(exclude_unset=True)
    for key,value in update_data.items():
        if value is not None:
            existing_patient[key] = value
    existing_patient['id'] = patient_id
    patient_obj = Patient(**existing_patient)
    data[patient_id] = patient_obj.model_dump(exclude={'id'})
    save_data(data)
    return {"message": f"Patient with ID {patient_id} updated successfully."}

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found.")
    del data[patient_id]
    save_data(data)
    return HTTPResponse(status_code=200, content={"message": f"Patient with ID {patient_id} deleted successfully."})