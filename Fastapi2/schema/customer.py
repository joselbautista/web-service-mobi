from pydantic import BaseModel
from typing import List
#from typing import Optional

class Customer(BaseModel):
        cod_app: str
        name: str
        vat: str
        phone: str
        mobile: str
        email: str
        street: str
        street2: str
        zip: str
        city: str
        state_name: str
        country: str
        stage_key: str
        payment_date: str
        payment_state: str
        payment_amount: str

class CustomersList(BaseModel):
    customers: List[Customer]