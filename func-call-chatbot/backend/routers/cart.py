from fastapi import APIRouter, Request
from routers.middleware import KnownAppError
from models.database import Database
from schemas.cart import CartItem
from fastapi.responses import JSONResponse
from supabase_client import get_supabase_client, get_access_token
from fastapi import Body

router = APIRouter()
BASE_DIR = "../mock-db"
database = Database()

@router.get("/cart")
def get_cart_items(request: Request):
    try:
        access_token = get_access_token(request=request)
        result = database.get_cart_items(access_token=access_token)
        return JSONResponse(content=result)
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)

@router.post("/cart/add")
async def add_to_cart(item: CartItem, request: Request):
    access_token = get_access_token(request=request)
    print(access_token)
    try:
        result = database.add_to_cart(
            variant_id=item.variant_id,
            quantity=item.quantity,
            access_token=access_token
        )
        return {"success": True, "message": "Item added to cart", "data": result}
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)

@router.patch("/cart/item/{cart_item_id}")
async def update_cart_item(cart_item_id: str, quantity: int = Body(...), request: Request = None):
    access_token = get_access_token(request=request)
    try:
        result = database.update_cart_item(cart_item_id=cart_item_id, quantity=quantity, access_token=access_token)
        return {"success": True, "message": "Cart item updated", "data": result}
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)

@router.delete("/cart/item/{cart_item_id}")
async def delete_cart_item(cart_item_id: str, request: Request = None):
    access_token = get_access_token(request=request)
    try:
        result = database.delete_cart_item(cart_item_id=cart_item_id, access_token=access_token)
        return {"success": True, "message": "Cart item deleted", "data": result}
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)

@router.get("/cart/user")
def get_user_cart(request: Request):
    access_token = get_access_token(request=request)
    try:
        result = database.get_user_cart(access_token=access_token)
        return JSONResponse(content=result)
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)