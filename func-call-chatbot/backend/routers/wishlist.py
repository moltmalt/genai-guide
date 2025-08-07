from fastapi import APIRouter, Request
from routers.middleware import KnownAppError
from models.database import Database
from fastapi.responses import JSONResponse
from supabase_client import get_access_token

router = APIRouter()
database = Database()

@router.get("/wishlist")
def get_wishlist_items(request: Request):
    try:
        access_token = get_access_token(request=request)
        result = database.get_wishlist_items(access_token=access_token)
        return JSONResponse(content=result)
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)

@router.post("/wishlist/add")
async def add_to_wishlist(request: Request):
    try:
        access_token = get_access_token(request=request)
        
        # Get the request body
        body = await request.json()
        variant_id = body.get("variant_id")
        
        if not variant_id:
            raise KnownAppError("variant_id is required", status_code=400)
        
        result = database.add_to_wishlist(variant_id=variant_id, access_token=access_token)
        return {"success": True, "message": "Item added to wishlist", "data": result}
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)

@router.delete("/wishlist/remove")
async def remove_from_wishlist(request: Request):
    try:
        access_token = get_access_token(request=request)
        # Get the request body
        body = await request.json()
        variant_id = body.get("variant_id")
        
        if not variant_id:
            raise KnownAppError("variant_id is required", status_code=400)
        
        result = database.remove_from_wishlist(variant_id=variant_id, access_token=access_token)
        return {"success": True, "message": "Item removed from wishlist", "data": result}
    except Exception as e:
        raise KnownAppError(str(e), status_code=500) 