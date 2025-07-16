from decimal import Decimal
from pydantic import BaseModel

class CartItem(BaseModel):
    name: str
    quantity: int
    size: str
    color: str
    price: Decimal

