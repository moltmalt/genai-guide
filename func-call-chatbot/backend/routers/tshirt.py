from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.database import Database
from schemas.tshirt import TShirtRequest
from routers.middleware import KnownAppError
from supabase_client import get_supabase_client

import os, json

router = APIRouter()
database = Database()

@router.get("/tshirts")
def get_all_shirts():
    result = database.get_all_shirts()
    return JSONResponse(content=result)

@router.post("/tshirts/search")
async def get_t_shirt(request: TShirtRequest):
    try:
        result = database.get_t_shirt(
            name =  request.name,
            size = request.size,
            color = request.color
        )
        return JSONResponse(content=result)
    except Exception as e:
        KnownAppError(str(e), status_code=500)
