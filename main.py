from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from prometheus_fastapi_instrumentator import Instrumentator
from models import (
    TokenInfo, 
    ProfileReturn, 
    ProfileUpdate,
    UserCreate,
    AuthCreate,
    ProfileCreate
)
from fastapi.security import OAuth2PasswordRequestForm
import utils
import httpx
import uvicorn

app = FastAPI(title="Client API Gateway", version="1.0.0")

@app.get("/health", summary="HealthCheck EndPoint", tags=["Health Check"])
def healthcheck():
    return {"status": "OK"}


@app.post("/login", response_model=TokenInfo, status_code=status.HTTP_200_OK)
async def login(
    auth_data: OAuth2PasswordRequestForm = Depends()
):
    result = await utils.process_login(auth_data)
    return TokenInfo(
        access_token=result.get('access_token'),
        token_type=result.get('token_type')
    )


@app.get("/profile/{req_uname}", response_model=ProfileReturn, status_code=status.HTTP_200_OK)
async def get_profile (
    req_uname: str,
    token_payload: dict = Depends(utils.get_current_token_payload) 
):
    result = await utils.get_profile(req_uname, token_payload) 
    return result


@app.put("/profile/{req_uname}", response_model=ProfileReturn, status_code=status.HTTP_200_OK)
async def change_profile (
    req_uname: str,
    profile_upd: ProfileUpdate,
    token_payload: dict = Depends(utils.get_current_token_payload) 
):
    result = await utils.update_profile(
        req_uname,
        profile_upd,
        token_payload
    )
    return result


@app.post("/register", response_model=ProfileReturn, status_code=status.HTTP_201_CREATED)
async def create_new_user (
    reg_data: UserCreate
):
    auth = AuthCreate(
        username = reg_data.username,
        password = reg_data.password, 
    )   
    
    # Если не получится - изнутри шибанет исключением    
    await utils.create_new_auth(auth)

    profile = ProfileCreate(
        username = reg_data.username,
        firstName = reg_data.firstName,
        lastName = reg_data.lastName,
        email = reg_data.email,
        phone = reg_data.phone
    )

    try:
        profile = await utils.create_new_profile(profile)
    except HTTPException as e:
        # TODO
        # Надо бы удалить созданного юзера в Auth сервисе, если тут не взлетело, но удаление в нем сейчас только авторизованным...
        # Когда-нибудь тут появится отправка запроса с внутренним токеном кубера, а в Auth - служебный эндпойнт с контролем этого токена
        # НО ТОЛЬКО НЕ СЕГОДНЯ! (с)
        raise e

    return profile


    

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)