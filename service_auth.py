
from config import settings
from models import AuthCreate
import httpx
from fastapi.security import OAuth2PasswordRequestForm
from service import Service


class AuthService(Service):
    def __init__(self):
        self._build_base_url(
            host = settings.auth_url.host,
            port = settings.auth_url.port 
        )


    async def create_auth(
        self, 
        username: str,
        password: str
    ):
        url = self._build_endpoint_url(settings.auth_url.register_endpoint)
        
        new_auth = AuthCreate(
            username = username,
            password = password, 
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json = new_auth.model_dump()
            )

        self._check_response(response)

        return response


    async def delete_auth(
        self,
        username: str
    ):
        url = self._build_endpoint_url(settings.auth_url.unregister_endpoint, username)

        async with httpx.AsyncClient() as client:
            response = await client.delete(url)

        self._check_response(response)

        return response


    async def login(
        self,
        auth_data: OAuth2PasswordRequestForm
    ):
        url = self._build_endpoint_url(endpoint = settings.auth_url.login_endpoint)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                data={
                    "username": auth_data.username,
                    "password": auth_data.password
                }
            )

        self._check_response(response)

        return response
    
