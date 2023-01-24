from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.jwt_manager import create_token
from schemas.user import User

user_router = APIRouter()

@user_router.post('/login', tags = ['auth'], status_code = 200, response_model = dict)
def login(user: User) -> dict:
    if user.email == "email" and user.password == "pass":
        token = create_token(user.dict())
        return JSONResponse(content = token, status_code = 200)
    return JSONResponse(content = {'error' : 'invalid user'}, status_code = 400)