from config import settings
from models import AuthCreate, ProfileCreate, ProfileUpdate, WalletCreate, TransactionCreate, OrderCreate, OrderUpdateEvent
import httpx
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status
from decimal import Decimal
from uuid import UUID


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
            amount = str(amount)
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json = new_transaction.model_dump()
            )

        self._check_response(response)

        return response
    

class OrderService(Service):
    def __init__(self):
        self._build_base_url(
            host = settings.order_url.host,
            port = settings.order_url.port 
        )

    
    async def create_order(
        self,
        username: str,
        price: Decimal
    ):
        url = self._build_endpoint_url(settings.order_url.create_endpoint)

        new_order = OrderCreate(
            username = username,
            price    = str(price)
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json = new_order.model_dump()
            )

        self._check_response(response)

        return response
    

    async def __push_event(
        self,
        event: OrderUpdateEvent
    ):
        url = self._build_endpoint_url(settings.order_url.event_endpoint)        

        async with httpx.AsyncClient() as client:
            response = await client.put(
                url,
                json = event.model_dump()
            )

        self._check_response(response)

        return response


    async def payment_confirmed(
        self,
        order_id: UUID,
        payment_id: UUID
    ):
        paid_event = OrderUpdateEvent(
            id         = str(order_id),
            event      = 'payment_confirmed',
            payment_id = str(payment_id)
        )
        
        response = await self.__push_event(paid_event)

        return response


    async def payment_failed(
        self,
        order_id: UUID
    ):
        failure_event = OrderUpdateEvent(
            id    = order_id,
            event = 'payment_failed'
        )

        response = await self.__push_event(failure_event)

        return response
    

    async def get_order_by_id(
        self,
        order_id: UUID
    ):
        url = self._build_endpoint_url(settings.order_url.get_by_id_endpoint, order_id)

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        self._check_response(response)

        return response
    

    async def get_orders_by_uname(
        self,
        req_uname: str
    ):
        url = self._build_endpoint_url(settings.order_url.get_by_user_endpoint, req_uname)

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        self._check_response(response)

        return response
    

class NotificationService(Service):
    def __init__(self):
        self._build_base_url(
            host = settings.notif_url.host,
            port = settings.notif_url.port 
        )
    

    async def get_notifications_for_order_id(
        self,
        order_id: UUID
    ):
        url = self._build_endpoint_url(settings.notif_url.get_by_order_id_endpoint, order_id)

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        self._check_response(response)

        return response
