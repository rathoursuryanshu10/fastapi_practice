from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Annotated,Literal
from pydantic import BaseModel, Field,computed_field
import joblib
import pandas as pd

app = FastAPI()

# Load the model
model = joblib.load("model.joblib")

class userInput(BaseModel):
    age: Annotated[int,Field(...,description='Age of user: ',gt=0,lt=120)]
    weight: Annotated[float,Field(...,description='Weight of user: ',gt=0)]
    height: Annotated[float,Field(...,description='Height of user: ',gt=0,lt=2.5)]
    income_lpa: Annotated[float,Field(...,description='Annual salary of the user: ',gt=0)]
    smoker: Annotated[bool,Field(...,description="True or False ")]
    city: Annotated[str,Field(...,description='city of the user from he/she belogs')]
    occupation: Annotated[Literal['Teacher', 'Doctor', 'Artist', 'Analyst', 'Engineer', 'Lawyer',
       'Business'],Field(...,description="Occupation of the user")]
    @computed_field
    @property
    def bmi(self)->float:
        return self.weight/(self.height**2)
    @computed_field
    @property
    def lifestyle_risk(self)->str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
    @computed_field
    @property
    def  age_group(self)->str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior" 
    @computed_field
    @property
    def city_tier(self)->int:
        tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
        tier_2_cities = [
            "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
            "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
            "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
            "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
            "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
            "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
        ]
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
    
user_data= {'age':32,'weight':67.5,'height':1.645,'income_lpa':2.4,'smoker':False,'city':'Delhi','occupation':'Engineer'}

user_obj = userInput(**user_data)

@app.post('/predict')
def predict(data:userInput):
    income_df = pd.DataFrame([{
        'age_group':data.age_group,
        'lifestyle_risk':data.lifestyle_risk,
        'occupation':data.occupation,
        'city_tier':data.city_tier,
        'bmi' : data.bmi,
        'income_lpa' :data.income_lpa
    }])
    prediction = model.predict(income_df)[0]
    return JSONResponse(status_code=200,content={'predicted_category':prediction})

