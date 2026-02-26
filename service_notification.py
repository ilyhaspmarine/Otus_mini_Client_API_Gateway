from config import settings
import httpx
from service import Service
from uuid import UUID


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
        url = self._build_endpoint_url(settings.notif_url.get_by_order_id_endpoint, str(order_id))

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        self._check_response(response)

        return response
