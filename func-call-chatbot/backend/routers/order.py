from fastapi import APIRouter, Request, Body
from fastapi.responses import JSONResponse
from models.database import Database
from schemas.cart import CartItem
from routers.middleware import KnownAppError
from supabase_client import get_access_token
import os, json

router = APIRouter()
BASE_DIR = "../mock-db"
database = Database()

@router.get("/order")
def get_order():
    file_path = os.path.join(BASE_DIR, "order.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    return JSONResponse(data)

@router.post("/order/place")
async def place_order(request: Request):
    try:
        access_token = get_access_token(request=request)
        result = database.place_order(access_token=access_token)
        return {"success": True, "message": "Order placed successfully", "data": result}
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)

@router.patch("/order/{order_id}")
async def update_order(order_id: str, status: str = Body(...), total_amount: float = Body(...), request: Request = None):
    access_token = get_access_token(request=request)
    try:
        result = database.update_order(order_id=order_id, status=status, total_amount=total_amount, access_token=access_token)
        return {"success": True, "message": "Order updated", "data": result}
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)

@router.delete("/order/{order_id}")
async def delete_order(order_id: str, request: Request = None):
    access_token = get_access_token(request=request)
    try:
        result = database.delete_order(order_id=order_id, access_token=access_token)
        return {"success": True, "message": "Order deleted", "data": result}
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)

@router.patch("/order/item/{order_item_id}")
async def update_order_item(order_item_id: str, quantity: int = Body(...), item_price: float = Body(...), request: Request = None):
    access_token = get_access_token(request=request)
    try:
        result = database.update_order_item(order_item_id=order_item_id, quantity=quantity, item_price=item_price, access_token=access_token)
        return {"success": True, "message": "Order item updated", "data": result}
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)

@router.delete("/order/item/{order_item_id}")
async def delete_order_item(order_item_id: str, request: Request = None):
    access_token = get_access_token(request=request)
    try:
        result = database.delete_order_item(order_item_id=order_item_id, access_token=access_token)
        return {"success": True, "message": "Order item deleted", "data": result}
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)

@router.get("/order/user")
def get_user_orders(request: Request):
    access_token = get_access_token(request=request)
    try:
        result = database.get_user_orders(access_token=access_token)
        return JSONResponse(content=result)
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)
