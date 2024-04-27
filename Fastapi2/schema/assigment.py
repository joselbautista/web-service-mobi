from pydantic import BaseModel
#from typing import Optional

class product_assignment(BaseModel):
    lot_id: str
    partner_id: str
    location_id: str
    date: str