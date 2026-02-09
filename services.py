from config import settings
from models import AuthCreate, ProfileCreate, ProfileUpdate, WalletCreate, TransactionCreate
import httpx
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status
from decimal import Decimal


class Service:
    def __init__(self):
        self._base_url = ""

    def _build_base_url(
        self,
        host: str = None,
        port: str = None,
        endpoint: str = None,
        param: str = None
    ):
        url = "http://"
        if host is not None:
            url += host
        if port is not None:
            url += ':' + port
        if endpoint is not None:
            url += '/' + endpoint
        if param is not None:
            url += '/' + param
        print(url)
        self._base_url = url

    def _check_response(
        self,
        response
    ):
        if not response.is_success:
            raise HTTPException(
                status_code=response.status_code, 
                detail=response.text
            )
        

    def _build_endpoint_url(
        self,
        endpoint: str = None,
        param: str = None
    ):
        url = self._base_url
        if endpoint is not None:
            url += '/' + endpoint
        if param is not None:
            url += '/' + param
        print(url)
        return url


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
    

class ProfileService(Service):
    def __init__(self):
        self._build_base_url(
            host = settings.prof_url.host,
            port = settings.prof_url.port 
        )

    
    async def create_profile(
        self,
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        phone: str
    ):
        url = self._build_endpoint_url(settings.prof_url.register_endpoint)

        new_profile = ProfileCreate(
            username = username,
            firstName = first_name,
            lastName = last_name,
            email = email,
            phone = phone
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json = new_profile.model_dump()
            )

        self._check_response(response)

        return response


    async def delete_profile(
        self,
        username: str
    ):
        url = self._build_endpoint_url(settings.prof_url.del_endpoint, username)

        async with httpx.AsyncClient() as client:
            response = await client.delete(url)

        self._check_response(response)

        return response
    

    async def get_profile(
        self,
        username: str
    ):
        url = self._build_endpoint_url(settings.prof_url.get_endpoint, username)

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        self._check_response(response)

        return response

        
    async def upd_profile(
        self,
        username: str,
        profile_upd: ProfileUpdate
    ):
        url = self._build_endpoint_url(settings.prof_url.upd_endpoint, username)

        async with httpx.AsyncClient() as client:
            response = await client.put(
                url,
                json = profile_upd.model_dump()
            )

        self._check_response(response)

        return response 


class BillingService(Service):
    def __init__(self):
        self._build_base_url(
            host = settings.bill_url.host,
            port = settings.bill_url.port 
        )


    async def create_wallet(
        self,
        username: str
    ):
        url = self._build_endpoint_url(settings.bill_url.register_endpoint)

        new_wallet = WalletCreate(
            username = username
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json = new_wallet.model_dump()
            )

        self._check_response(response)

        return response


    async def delete_wallet(
        self,
        username: str    
    ):
        #Удаление так-то не предполагается, ибо кошелек - это финал саги
        pass


    async def get_wallet(
        self,
        username: str
    ):
        url = self._build_endpoint_url(settings.bill_url.wallet_get_endpoint, username)

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        self._check_response(response)

        return response


    async def create_transaction(
        self, 
        username: str,
        amount: Decimal
    ):
        url = self._build_endpoint_url(settings.bill_url.transaction_endpoint)

        new_transaction = TransactionCreate(
            username = username,
            amount = amount
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json = new_transaction.model_dump()
            )

        self._check_response(response)

        return response