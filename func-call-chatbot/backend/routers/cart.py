from fastapi import APIRouter
from routers.middleware import KnownAppError
from models.tshirt import TShirtDatabase
from schemas.cart import CartItem
from fastapi.responses import JSONResponse

import os, json

router = APIRouter()
BASE_DIR = "func-call-chatbot/mock-db"
database = TShirtDatabase()

@router.get("/cart")
def get_cart():
    file_path = os.path.join(BASE_DIR, "cart.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    return JSONResponse(data)

@router.post("/cart/add")
async def add_to_cart(item: CartItem):
    try:
        result = database.get_t_shirts(
            name = item.name,
            quantity = item.quantity,
            size = item.size,
            color = item.color,
            price = item.price
        )
        return {"success": True, "message": "Item added to cart" ,"data": result}
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)