from config import settings
from models import WalletCreate, TransactionCreate
import httpx
from service import Service
from decimal import Decimal
from uuid import UUID

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
    

    async def storno_transaction(
        self,
        transaction_id: UUID
    ):
        url = self._build_endpoint_url(settings.bill_url.storno_endpoint, str(transaction_id))

        async with httpx.AsyncClient() as client:
            response = await client.post(url)

        self._check_response(response)

        return response