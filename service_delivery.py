from config import settings
from models import CourierCreate, DeliveryCreate
from service import Service
import httpx
from uuid import UUID


class DeliveryService(Service):
    def __init__(self):
        self._build_base_url(
            host = settings.deliv_url.host,
            port = settings.deliv_url.port 
        )


    async def create_courier(
        self,
        new_courier: CourierCreate
    ):
        url = self._build_endpoint_url(settings.deliv_url.courier_create_endpoint)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json = new_courier.model_dump()
            )

        self._check_response(response)

        return response
    

    async def create_delivery(
        self,
        order_id: UUID,
        address: str
    ):
        url = self._build_endpoint_url(settings.deliv_url.delivery_create_endpoint)

        new_delivery = DeliveryCreate(
            order_id = str(order_id),
            address = address 
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json = new_delivery.model_dump()
            )

        self._check_response(response)

        return response
    

    async def cancel_delivery(
        self,
        order_id: UUID
    ):
        url = self._build_endpoint_url(settings.deliv_url.delivery_cancel_endpoint, str(order_id))

        async with httpx.AsyncClient() as client:
            response = await client.put(url)

        self._check_response(response)

        return response
    

    async def get_delivery(
        self,
        order_id: UUID
    ):
        url = self._build_endpoint_url(settings.deliv_url.delivery_get_endpoint, str(order_id))

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        self._check_response(response)

        return response