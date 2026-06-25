from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator
from typing import Annotated, List,Dict, Optional,Annotated

# Pydantic model (class) to represent the schema 
class Patient(BaseModel):
    name: str 
    email: EmailStr
    linked_in: Optional[AnyUrl] = None
    age: int # = Field(gt=0,lt=100, description="Age must be between 1 and 99")
    weight: Annotated[float,Field(default=None,gt=0, strict=True)]
    married: bool= False
    allergies: Optional[List[str]] = None # it is older way(required to import List from typing) | allergies: list[str] # it is newer way
    contact_details: dict[str, str] # it is modern way | contact_details: Dict[str, str] # it is older way(required to import Dict from typing)

    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains = ['probyto.com', 'lazyanalyst.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError(f"Email domain must be one of {valid_domains}")
        return value
    
    @field_validator('name')
    @classmethod
    def name_capitalization(cls,value):
        return value.upper()
    
    @field_validator('age', mode='after')
    @classmethod
    def age_validator(cls,value):
        if value <= 0 or value >= 100:
            raise ValueError("Age must be between 1 and 99")
        return value
# raw input data (dictionary or JSON) representing a patient
patient_info = {'name': "John Doe", 'email': 'john.doe@probyto.com', 'linked_in': 'https://www.linkedin.com/in/johndoe', 'age': '30', 'weight': 70.5, 'married': True, 'allergies': ['penicillin', 'peanuts'], 'contact_details': {'email': 'john.doe@example.com', 'phone_no': '123-456-7890'}}

# Create a Patient instance(object) using the patient_info dictionary
patient1 = Patient(**patient_info)

def insert_patient_data(patient_data: Patient):
    print(f"Patient Name: {patient_data.name}")
    print(f"Email: {patient_data.email}")
    print(f"Linked-in: {patient_data.linked_in}")
    print(f"Age: {patient_data.age}")
    print(f"Weight: {patient_data.weight}")
    print(f"Married: {patient_data.married}")
    print(f"Allergies: {', '.join(patient_data.allergies)}")
    print(f"Contact Details: Email - {patient_data.contact_details['email']}, Phone - {patient_data.contact_details['phone_no']}")
    print("Patient data inserted successfully!")

def update_patient_data(patient_data: Patient):
    print(f"Patient Name: {patient_data.name}")
    print(f"Email: {patient_data.email}")
    print(f"Linked-in: {patient_data.linked_in}")
    print(f"Age: {patient_data.age}")
    print(f"Weight: {patient_data.weight}")
    print(f"Married: {patient_data.married}")
    print(f"Allergies: {', '.join(patient_data.allergies)}")
    print(f"Contact Details: Email - {patient_data.contact_details['email']}, Phone - {patient_data.contact_details['phone_no']}")
    print("Patient data updated successfully!")

# insert_patient_data(patient1)
# data2 = {'name': "Jane Smith", 'age': 25}
# patient2 = Patient(**data2)
update_patient_data(patient1)