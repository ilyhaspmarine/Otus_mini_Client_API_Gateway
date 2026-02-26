from config import settings
from models import OrderCreate, OrderUpdateEvent
import httpx
from decimal import Decimal
from uuid import UUID
from service import Service

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
        url = self._build_endpoint_url(settings.order_url.get_by_id_endpoint, str(order_id))

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