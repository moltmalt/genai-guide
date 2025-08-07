from fastapi import APIRouter, Response
from models.customer import Customer
from routers.middleware import KnownAppError
from schemas.customer import SignInData

database = Customer()
router = APIRouter()

@router.post("/auth/sign_in")
async def sign_in(data: SignInData, response: Response):
    try:
        result = database.sign_in(data.email, data.password)
        response.set_cookie(key="access_token", value=result["access_token"], httponly=True)
        response.set_cookie(key="refresh_token", value=result["refresh_token"], httponly=True)

        return {
            "success": True, 
            "message": "Sign in succesfully",
            "data": result,
            "user_id": result["user"]["id"]
        }
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)

@router.get("/auth/sign_out")
async def sign_out():
    try:
        result = database.sign_out()
        return {"success": True, "message": "Sign out succesfully" ,"data": result}
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)
