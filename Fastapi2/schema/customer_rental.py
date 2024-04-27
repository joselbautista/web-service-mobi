from pydantic import BaseModel
from typing import List
#from typing import Optional

class Customer_rental(BaseModel):
        cod_app: str

class customer_rentalList(BaseModel):
    customer_rental: List[Customer_rental]