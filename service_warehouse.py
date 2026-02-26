from config import settings
from models import GoodCreate, ReservationCreate, StockCreate, ReservationPosCreate
from service import Service
import httpx
from uuid import UUID

class WarehouseService(Service):
    def __init__(self):
        self._build_base_url(
            host = settings.wareh_url.host,
            port = settings.wareh_url.port 
        )

    
    async def create_good(
        self, 
        new_good: GoodCreate,
    ):
        url = self._build_endpoint_url(settings.wareh_url.good_create_endpoint)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json = new_good.model_dump()
            )

        self._check_response(response)

        return response
    

    async def add_stock(
        self,
        new_stock: StockCreate
    ):
        url = self._build_endpoint_url(settings.wareh_url.stock_create_endpoint)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json = new_stock.model_dump()
            )

        self._check_response(response)

        return response
    

    async def create_reservation(
        self,
        order_id: UUID,
        order_positions
    ):
        url = self._build_endpoint_url(settings.wareh_url.reserve_create_endpoint)

        reservation_positions = []

        for pos in order_positions:
            reservation_positions.append(
                ReservationPosCreate(
                    good_id = str(pos.good_id),
                    quantity = pos.quantity
                )
            )

        new_reservation = ReservationCreate(
            order_id = str(order_id),
            positions = reservation_positions 
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json = new_reservation.model_dump()
            )

        self._check_response(response)

        return response


    async def cancel_reservation(
        self,
        order_id: UUID
    ):
        url = self._build_endpoint_url(settings.wareh_url.reserve_cancel_endpoint, str(order_id))

        async with httpx.AsyncClient() as client:
            response = await client.put(url)

        self._check_response(response)

        return response
    

    async def get_reservation_by_order_id(
        self,
        order_id: UUID
    ):
        url = self._build_endpoint_url(settings.wareh_url.reserve_get_endpoint, str(order_id))

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        self._check_response(response)

        return response
    

    async def get_stock_by_good_id(
        self,
        good_id: UUID
    ):
        url = self._build_endpoint_url(settings.wareh_url.stock_get_endpoint, str(good_id))

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        self._check_response(response)

        return response