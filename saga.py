from models import UserCreate, ProfileReturn, OrderCreate, OrderReturn
from services import AuthService, ProfileService, BillingService, OrderService
from fastapi import HTTPException
from uuid import UUID
from decimal import Decimal

class SagaRegister():

    def __init__(self):
        self.__auth_created    = False
        self.__profile_created = False
        self.__wallet_created  = False

    async def execute_saga(
        self,
        reg_data: UserCreate
    ):
        auth_service    = AuthService()
        profile_service = ProfileService()
        billing_service = BillingService()

        try:            
            auth_response = await auth_service.create_auth(reg_data.username, reg_data.password)
            self.__auth_created = True

            profile_response = await profile_service.create_profile(reg_data.username,
                                                                    reg_data.firstName,
                                                                    reg_data.lastName,
                                                                    reg_data.email,
                                                                    reg_data.phone)
            self.__profile_created = True

            billing_response = await billing_service.create_wallet(reg_data.username)
            self.__wallet_created = True

        except Exception as e:
            print('Ошибка при регистрации: ' + str(e))
            await self.rollback_saga(reg_data)
            raise

        json = profile_response.json()
        return ProfileReturn(
            username  = json.get("username"),
            email     = json.get("email"),
            phone     = json.get("phone"),
            firstName = json.get("firstName"),
            lastName  = json.get("lastName")
        )


    async def rollback_saga(
        self,
        reg_data: UserCreate
    ):
        auth_service    = AuthService()
        profile_service = ProfileService()
        billing_service = BillingService()

        try:
            if self.__wallet_created:
                billing_response = billing_service.delete_wallet(reg_data.username)
                self.__wallet_created = False
            if self.__profile_created:
                profile_response = await profile_service.delete_profile(reg_data.username)
                self.__profile_created = False
            if self.__auth_created:
                auth_response = await auth_service.delete_auth(reg_data.username)
                self.__auth_created = False
        except Exception as e:
            print('Ошибка при откате регистрации: ' + str(e))
            raise


class SagaOrder:
    def __init__(self):
        self.__order_id = None
        self.__payment_id = None
        self.__order_status_set = False

    
    async def execute_saga(
        self,
        order_data: OrderCreate
    ):
        order_service = OrderService()
        billing_service = BillingService()

        try:
            order_response = await order_service.create_order(order_data.username, order_data.price)
            self.__order_id = order_response.json().get('id')

            tr_amount = -Decimal(order_data.price)
            billing_response = await billing_service.create_transaction(order_data.username, tr_amount)
            self.__payment_id = billing_response.json().get('id')

            status_response = await order_service.payment_confirmed(self.__order_id, self.__payment_id)
            self.__order_status_set = True

        except Exception as e:
            print(f'Ошибка при оформлении заказа: {e}')
            status_response = await self.rollback_saga(order_data)
            # raise

        json = status_response.json()
        return OrderReturn(
            id = UUID(json.get('id')),
            username = json.get('username'),
            price = json.get('price'),
            status = json.get('status'),
            placed_at = json.get('placed_at'),
            updated_at = json.get('updated_at')
        )


    async def rollback_saga(
        self,
        order_data: OrderCreate
    ):
        order_service = OrderService()
        billing_service = BillingService()

        try:
            if self.__order_status_set:
                # Как бе нечего откатывать, финальный шаг был
                self.__order_status_set = False
                pass
            if self.__payment_id:
                # Откат транзакции реализуется новой транзакцией с противоположным знаком
                tr_amount = Decimal(order_data.price)
                billing_response = await billing_service.create_transaction(order_data.username, tr_amount)
                self.__payment_id = None
                pass
            if self.__order_id:
                status_response = await order_service.payment_failed(self.__order_id)
                return status_response
        except Exception as e:
            print(f'Ошибка при откате заказа: {e}')
            raise