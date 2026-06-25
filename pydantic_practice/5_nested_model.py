from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class Patient(BaseModel):
    name: str 
    age: int
    gender: str
    address: Address
address_info = {
    'street': '123 Main St',
    'city': 'Anytown',
    'state': 'CA',
    'zip_code': '12345'
}
address1= Address(**address_info)
patient_info = {
    'name': "John Doe",
    'age': 30,
    'gender': 'Male',
    'address': address1
}
patient1= Patient(**patient_info)

def insert_patient_data(patient_data: Patient):
    print(f"Patient Name: {patient_data.name}")
    print(f"Age: {patient_data.age}")
    print(f"Gender: {patient_data.gender}")
    print(f"Address: {patient_data.address.street}, {patient_data.address.city}, {patient_data.address.state} {patient_data.address.zip_code}")
    print("Patient data inserted successfully!")
insert_patient_data(patient1)