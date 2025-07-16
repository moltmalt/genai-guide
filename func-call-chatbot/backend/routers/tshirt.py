from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.tshirt import TShirtDatabase
from schemas.tshirt import TShirtRequest
from routers.middleware import KnownAppError

import os, json

router = APIRouter()
BASE_DIR = "func-call-chatbot/mock-db"
database = TShirtDatabase()

@router.get("/tshirts")
def get_all_shirts():
    file_path = os.path.join(BASE_DIR, "shirt.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    return JSONResponse(data)

@router.post("/tshirts/search")
async def get_t_shirts(request: TShirtRequest):
    try:
        result = database.get_t_shirts(
            name = request.name,
            size = request.size,
            color =  request.color
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise KnownAppError(str(e), status_code = 500)