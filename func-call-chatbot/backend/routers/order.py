from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.tshirt import TShirtDatabase
from schemas.cart import CartItem
from routers.middleware import KnownAppError

import os, json

router = APIRouter()
BASE_DIR = "func-call-chatbot/mock-db"
database = TShirtDatabase()

@router.get("/order")
def get_order():
    file_path = os.path.join(BASE_DIR, "order.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    return JSONResponse(data)

@router.post("/order/place")
async def place_order(item: CartItem):
    try:
        result = database.place_order(
            name = item.name,
            quantity = item.quantity,
            size = item.size,
            color = item.color,
            price = item.price
        )
        return {"success": True, "message": "Order placed succesfully" ,"data": result}
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)
