from pydantic import BaseModel,EmailStr, AnyUrl,Field,field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class patient(BaseModel) :
    name:str =Annotated[str, Field(max_length=40,title="patient name",description='give the name of patient in less then 40 chars',examples=['ranjeet','nitish'])]
    email: EmailStr
    github_url: AnyUrl
    age:int
    weight:Annotated[float, Field(gt=0, lt=120,strict=True)]
    height:float
    married:bool =Annotated[bool,Field(default=None,description='is patient married or not ')]
    allergies:Optional[list[str]] = None
    contact_details:dict[str, str]

    ## field validator 
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domain = ['hdfc.com','icici.com']
        # abc@gmail.com
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domain:
            raise ValueError ("not a valid domain")

        return value

    ## model validator

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency_contact' not in model.contact_details:
            raise ValueError('patient older than 60 must be have an emergency contact')
        return model

    ## computed field
    @computed_field
    @property 
    def bmi(self) -> float:
        bmi = round((self.weight)/(self.height**2),2)
        return bmi

def insert_patient_data(patient:patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.weight)
    print(patient.height)
    print("BMI",patient.bmi)
    print(patient.married)
    print(patient.contact_details)
    print("Created Successed")



patient_info ={'name':'Ranjeet',
               'email':'abc@hdfc.com',
               'github_url':'https://github.com/Ranjeetshah1548',
               'age':62,
               'weight':40 ,
               'height': 1.75,
               'allergies':['dust','dust'],
               'contact_details':{'email':'ranjit777@hdfc.com','emergency_contact':"55454512515"}
               }

p1 = patient(**patient_info)

insert_patient_data(p1)