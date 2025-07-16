from pydantic import BaseModel
from decimal import Decimal

class OrderRequest(BaseModel):
    name: str
    quantity: int
    size: str
    color: str
    price: Decimal