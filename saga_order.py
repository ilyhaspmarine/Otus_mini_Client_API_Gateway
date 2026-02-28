from models import OrderCreate, OrderReturn, OrderCreateStatusReturn
from service_billing import BillingService
from service_order import OrderService
from service_delivery import DeliveryService
from service_warehouse import WarehouseService
from uuid import UUID
from decimal import Decimal
from saga_db_schema import SagaOrder as SagaOrder_DB, SagaStatus
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import datetime
import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select, and_, func
from sqlalchemy.future import select


class SagaOrder:
    def __init__(self):
        self.__order_id = None
        self.__payment_id = None
        self.__order_status_set = False
        self.__reservation_id = None
        self.__delivery_id = None


    async def __init_new_saga(
        self,
        db: AsyncSession
    ):
        new_saga = SagaOrder_DB(
            id = uuid.uuid4(),
            status = SagaStatus.UNFINISHED,
            last_updated = datetime.utcnow()
        )

        db.add(new_saga)

        try:
            await db.commit()
            id = new_saga.id
            result = await db.execute(
                select(SagaOrder_DB)
                .filter(SagaOrder_DB.id == id)
                .with_for_update()
            )
            new_saga = result.scalar_one_or_none()
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = 'Failed to create new order')
        except Exception as e:
            print(f"=== EXCEPTION ===")
            print(f"Type: {type(e).__name__}")
            print(f"Message: {e}")
            # Самое важное:
            print(f"ORIG: {e.orig}") 
            await db.rollback()
            raise
        return new_saga
    

    async def __update_db_saga(
        self,
        db: AsyncSession,
        saga: SagaOrder_DB,
    ):
        # if order_id is not None:
        #     saga.order_id = order_id
        # if order_cancelled is not None:
        #     saga.order_cancelled = order_cancelled
        # if payment_id is not None:
        #     saga.payment_id = payment_id
        # if payment_cancelled is not None:
        #     saga.payment_cancelled = payment_cancelled
        # if reservation_id is not None:
        #     saga.reservation_id = reservation_id
        # if reservation_cancelled is not None:
        #     saga.reservation_cancelled = reservation_cancelled
        # if delivery_id is not None:
        #     saga.delivery_id = delivery_id
        # if delivery_cancelled is not None:
        #     saga.delivery_cancelled = delivery_cancelled
        saga.last_updated = datetime.utcnow()
        await db.commit()
        id = saga.id
        saga = await db.execute(
            select(SagaOrder_DB)
            .filter(SagaOrder_DB.id == id)
            .with_for_update()
        )
        
        return saga

    
    async def execute_saga(
        self,
        order_data: OrderCreate,
        db: AsyncSession
    ):
        # Запишем новую сагу в БД (чтобы была возможность потом отследить недобитые саги)
        new_saga = await self.__init_new_saga(db)

        order_service = OrderService()
        billing_service = BillingService()
        warehouse_service = WarehouseService()
        delivery_service = DeliveryService()

        result = OrderCreateStatusReturn()

        try:
            # Если кто-то из сервисов недоступен - сага провалена и должна откатиться
            order_response = await order_service.create_order(order_data.username, order_data.price)
            new_saga.order_id = order_response.json().get('id')
            new_saga = await self.__update_db_saga(db, new_saga)

            tr_amount = -Decimal(order_data.price)
            billing_response = await billing_service.create_transaction(order_data.username, tr_amount)
            new_saga.payment_id = billing_response.json().get('id')
            new_saga = await self.__update_db_saga(db, new_saga)

            warehouse_response = await warehouse_service.create_reservation(new_saga.order_id, order_data.positions)
            new_saga.reservation_id = warehouse_response.json().get('id')
            new_saga = await self.__update_db_saga(db, new_saga)

            delivery_response = await delivery_service.create_delivery(new_saga.order_id, order_data.address)
            new_saga.delivery_id = delivery_response.json().get('id')
            new_saga = await self.__update_db_saga(db, new_saga)

            status_response = await order_service.payment_confirmed(new_saga.order_id, new_saga.payment_id)
            new_saga.status = SagaStatus.COMPLETED
            new_saga = await self.__update_db_saga(db, new_saga)

        except Exception as e:
            result.error = f'Ошибка при оформлении заказа: {e}'
            print(result.error)
            await self.rollback_saga(new_saga.id, order_data, db)
            # raise

        if not new_saga.order_id is None:
            result.id = new_saga.order_id

        return result



    async def rollback_saga(
        self,
        saga_id: UUID,
        order_data: OrderCreate,
        db: AsyncSession
    ):
        
        async_session_factory = db.bind.registry 

        await asyncio.create_task(
            self._perform_rollback_with_retries_per_step(saga_id, order_data, async_session_factory)
        )

    async def _perform_rollback_with_retries_per_step(
        self,
        saga_id: UUID,
        order_data: OrderCreate,
        session_factory: async_sessionmaker,
        max_retries: int = 3,
        base_delay: float = 1.0
    ):
        async with session_factory() as db:
            # Загружаем сагу для отката
            result = await db.execute(
                select(SagaOrder_DB)
                .filter(SagaOrder_DB.id == saga_id)
                .with_for_update()
            )
            saga = result.scalar_one_or_none()

            if saga is None:
                print("Сага не найдена для отката.")
                return

            # Откатываем каждый шаг с повторными попытками
            if not saga.delivery_cancelled:
                delivery_service = DeliveryService()
                
                await self._retry_rollback_step(
                    lambda: delivery_service.cancel_delivery(saga.delivery_id),
                    "доставки",
                    max_retries=max_retries,
                    base_delay=base_delay
                )
                saga.delivery_cancelled = True
                saga = await self.__update_db_saga(db, saga)

            if not saga.reservation_cancelled:
                warehouse_service = WarehouseService()               
                await self._retry_rollback_step(
                    lambda: warehouse_service.cancel_reservation(saga.reservation_id),
                    "резервации",
                    max_retries=max_retries,
                    base_delay=base_delay
                )
                saga.reservation_cancelled = True
                saga = await self.__update_db_saga(db, saga) 

            if not saga.payment_cancelled:
                billing_service = BillingService()
                await self._retry_rollback_step(
                    lambda: billing_service.storno_transaction(saga.payment_id),
                    "платежа",
                    max_retries=max_retries,
                    base_delay=base_delay
                )
                saga.payment_cancelled = True
                saga = await self.__update_db_saga(db, saga) 

            if not saga.order_cancelled and saga.status != SagaStatus.COMPLETED:
                order_service = OrderService()
                await self._retry_rollback_step(
                    lambda: order_service.payment_failed(saga.order_id),
                    "статуса заказа",
                    max_retries=max_retries,
                    base_delay=base_delay
                )
                saga.order_cancelled = True
                saga.status = SagaStatus.CANCELLED
                saga = await self.__update_db_saga(db, saga)


    async def _retry_rollback_step(
        self,
        step_func: callable,
        step_name: str,
        max_retries: int = 3,
        base_delay: float = 1.0
    ):
        for attempt in range(max_retries):
            try:
                await step_func()
                print(f"Откат {step_name} выполнен успешно.")
                break
            except Exception as e:
                print(f"Ошибка при откате {step_name} (попытка {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"Ждём {delay} секунд перед повторной попыткой отката {step_name}...")
                    await asyncio.sleep(delay)
                else:
                    print(f"Все попытки отката {step_name} исчерпаны.")
                    raise