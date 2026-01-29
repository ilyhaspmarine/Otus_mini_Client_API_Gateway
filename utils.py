from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from config import settings
import jwt
import httpx
from models import (
    AuthCreate,
    ProfileCreate,
    ProfileReturn,
    ProfileUpdate
)

http_bearer = HTTPBearer()

def build_url(
    host: str = None,
    path: str = None,
    port: str = None,
    endpoint: str = None,
    param: str = None
):
    url = "http://"
    if host is not None:
        url += host
    # if path is not None:
    #     url += '/' + path 
    if port is not None:
        url += ':' + port
    if endpoint is not None:
        url += '/' + endpoint
    if param is not None:
        url += '/' + param
    print(url)
    return url

def check_response(
    response
):
    if not response.is_success:
        raise HTTPException(
            status_code=response.status_code, 
            detail=response.text
        )

def return_profile(
    response
):
    json = response.json()    
    return ProfileReturn(
        username  = json.get("username"),
        email     = json.get("email"),
        phone     = json.get("phone"),
        firstName = json.get("firstName"),
        lastName  = json.get("lastName")
    )

def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm]
    )
    return decoded

def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    token = credentials.credentials
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error",
        )

    return payload

async def process_login(
    auth_data: OAuth2PasswordRequestForm
):
    url = build_url(
        host = settings.auth_url.host,
        path = settings.auth_url.path,
        port = settings.auth_url.port,
        endpoint = settings.auth_url.login_endpoint
    )

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            data={
                "username": auth_data.username,
                "password": auth_data.password
            }
        )

    check_response(response)

    return response.json()

async def create_new_auth (
        new_auth: AuthCreate
):
    url = build_url(
        host = settings.auth_url.host,
        path = settings.auth_url.path,
        port = settings.auth_url.port,
        endpoint = settings.auth_url.register_endpoint 
    )

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json = new_auth.model_dump()
        )

    check_response(response)

async def create_new_profile(
    new_profile: ProfileCreate
):
    url = build_url(
        host = settings.prof_url.host,
        path = settings.prof_url.path,
        port = settings.prof_url.port,
        endpoint = settings.prof_url.register_endpoint
    )

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json = new_profile.model_dump()
        )

    check_response(response)

    return return_profile(response)

def check_token_uname(
    uname: str,
    token_payload: dict
):
    if uname != token_payload.get("sub"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access forbidden",
        )
    
async def get_profile(
    req_uname: str,
    token_payload: dict
):
    # Если не совпадет - изнутри шибанет исключением 
    check_token_uname(req_uname, token_payload)

    url = build_url(
        host = settings.prof_url.host,
        path = settings.prof_url.path,
        port = settings.prof_url.port,
        endpoint = settings.prof_url.get_endpoint,
        param = req_uname
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url
        )

    check_response(response)

    return return_profile(response)

async def update_profile(
    req_uname: str,
    profile_upd: ProfileUpdate,
    token_payload: dict
):
    # Если не совпадет - изнутри шибанет исключением 
    check_token_uname(req_uname, token_payload)

    url = build_url(
        host = settings.prof_url.host,
        path = settings.prof_url.path,
        port = settings.prof_url.port,
        endpoint = settings.prof_url.upd_endpoint,
        param = req_uname
    )

    async with httpx.AsyncClient() as client:
        response = await client.put(
            url,
            json = profile_upd.model_dump()
        )

    check_response(response) 
    
    json = response.json()

    return ProfileReturn(
        username  = req_uname,
        email     = json.get("email"),
        phone     = json.get("phone"),
        firstName = json.get("firstName"),
        lastName  = json.get("lastName")
    )
