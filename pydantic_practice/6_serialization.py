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

temp = patient1.model_dump()
print(temp)
print(type(temp))