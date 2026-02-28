from fastapi import Depends, FastAPI, HTTPException, status
from prometheus_fastapi_instrumentator import Instrumentator
from models import (
    TokenInfo,  
    UserCreate,
    ProfileReturn,
    ProfileUpdate,
    WalletReturn,
    TransactionReturn,
    TransactionCreate,
    OrderCreate,
    OrderReturn,
    OrderCreateStatusReturn,
    NotificationReturn,
    GoodReturn,
    GoodCreate,
    StockCreate,
    StockReturn,
    CourierCreate, 
    CourierReturn,
    SagaReturn, 
    DeliveryReturn,
    ReservationReturn
)
from fastapi.security import OAuth2PasswordRequestForm
import utils
from uuid import UUID
from typing import List
from db import _get_db

# import uvicorn

app = FastAPI(title="Client API Gateway", version="1.0.0")

@app.get("/health", summary="HealthCheck EndPoint", tags=["Health Check"])
def healthcheck():
    return {"status": "OK"}


@app.post("/login", summary = 'Login point for user', tags = ['Auth'], response_model=TokenInfo, status_code=status.HTTP_200_OK)
async def login(
    auth_data: OAuth2PasswordRequestForm = Depends()
):
    result = await utils.process_login(auth_data)
    return TokenInfo(
        access_token=result.get('access_token'),
        token_type=result.get('token_type')
    )


@app.get("/profile/{req_uname}", summary = 'Get User profile', tags = ['Profile'], response_model=ProfileReturn, status_code=status.HTTP_200_OK)
async def get_profile (
    req_uname: str,
    token_payload: dict = Depends(utils.get_current_token_payload) 
):
    result = await utils.get_profile(req_uname, token_payload) 
    return result


@app.put("/profile/{req_uname}", summary = 'Update User profile', tags = ['Profile'],  response_model=ProfileReturn, status_code=status.HTTP_200_OK)
async def change_profile (
    req_uname: str,
    profile_upd: ProfileUpdate,
    token_payload: dict = Depends(utils.get_current_token_payload) 
):
    result = await utils.update_profile(
        req_uname,
        profile_upd,
        token_payload
    )
    return result


@app.post("/register", summary = 'Register new User', tags = ['Auth'], response_model=ProfileReturn, status_code=status.HTTP_201_CREATED)
async def create_new_user (
    reg_data: UserCreate
):
    profile = await utils.process_register(reg_data)

    return profile


@app.get("/wallet/{req_uname}", summary = 'Create Wallet for User', tags = ['Billing', 'Wallet'], response_model = WalletReturn)
async def get_wallet(
    req_uname: str,
    token_payload: dict = Depends(utils.get_current_token_payload)
):
    wallet = await utils.get_wallet(req_uname, token_payload)

    return wallet


@app.post("/transaction", summary = 'Create billing transaction', tags = ['Billing', 'Transaction'], response_model = TransactionReturn)
async def create_transaction(
    tr_data: TransactionCreate,
    token_payload: dict = Depends(utils.get_current_token_payload)
):
    transaction = await utils.create_transaction(tr_data, token_payload)

    return transaction

@app.post("/orders", summary = 'Create order', tags = ['Orders'], response_model = OrderCreateStatusReturn, status_code = status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    token_payload: dict = Depends(utils.get_current_token_payload),
    db = Depends(_get_db)
):

    order = await utils.process_new_order(order_data, token_payload, db)

    return order


@app.get("/orders/id/{order_id}", summary = 'Get order by ID', tags = ['Orders'], response_model = OrderReturn)
async def get_order_by_id(
    order_id: UUID,
    token_payload: dict = Depends(utils.get_current_token_payload)
):
    order = await utils.get_order_by_id(order_id, token_payload)

    return order


@app.get("/orders/user/{req_uname}", summary = 'Get orders for user', tags = ['Orders'], response_model = List[OrderReturn])
async def get_orders_for_user(
    req_uname: str,
    token_payload: dict = Depends(utils.get_current_token_payload)
):
    orders = await utils.get_orders_by_uname(req_uname, token_payload)

    return orders


@app.get('/notifications/{order_id}', summary = 'Get notifications for order', tags = ['Notifications', 'Orders'], response_model = List[NotificationReturn])
async def get_notifications_for_order(
    order_id: UUID,
    token_payload: dict = Depends(utils.get_current_token_payload)
):
    notifications = await utils.get_notifications_for_order(order_id, token_payload)
    
    return notifications


@app.post('/goods', summary='Create new good', tags=['Warehouse', 'Goods'], response_model=GoodReturn, status_code = status.HTTP_201_CREATED)
async def good_create(
    good_data: GoodCreate,
    token_payload: dict = Depends(utils.get_current_token_payload)
):
    good = await utils.good_create(good_data)

    return good


@app.post('/stocks', summary='Add stock for good', tags=['Warehouse', 'Stocks'], response_model=StockReturn, status_code = status.HTTP_201_CREATED)
async def stock_add(
    stock_data: StockCreate,
    token_payload: dict = Depends(utils.get_current_token_payload)
):
    stock = await utils.stock_add(stock_data)

    return stock


@app.get('/stocks/{good_id}', summary='Get stock for good', tags=['Warehouse', 'Stocks'], response_model=StockReturn)
async def stock_get_by_good_id(
    good_id: UUID,
    token_payload: dict = Depends(utils.get_current_token_payload)
):
    stock = await utils.stock_get_by_good_id(good_id)

    return stock


@app.get('/reservations/{order_id}', summary='Get reservation for order', tags=['Warehouse', 'Reservations'], response_model=ReservationReturn)
async def reservation_get_by_order_id(
    order_id: UUID,
    token_payload: dict = Depends(utils.get_current_token_payload)
):
    reservation = await utils.reservation_get_by_order_id(order_id)

    return reservation


@app.post('/couriers', summary = 'Create new courier', tags=['Delivery', 'Couriers'], response_model = CourierReturn, status_code = status.HTTP_201_CREATED)
async def create_new_courier(
    courier_data: CourierCreate,
    token_payload: dict = Depends(utils.get_current_token_payload)
):
    courier = await utils.courier_create(courier_data)

    return courier


@app.get('/deliveries/{order_id}', summary='Get delivery for order', tags=['Warehouse', 'Stocks'], response_model = DeliveryReturn)
async def get_delivery_by_order_id(
    order_id: UUID,
    token_payload: dict = Depends(utils.get_current_token_payload)
):
    delivery = await utils.delivery_get_by_order_id(order_id)

    return delivery


@app.get('/sagas', summary = 'Get all order sagas', tags=['Saga'], response_model = List[SagaReturn])
async def get_sagas_list(
    db = Depends(_get_db)
):
    sagas = await utils.get_all_order_sagas(db)

    return sagas


@app.get('/sagas/{saga_id}', summary = 'Get order saga by ID', tags=['Saga'], response_model = SagaReturn)
async def get_sagas_list(
    saga_id: UUID,
    db = Depends(_get_db)
):
    saga = await utils.get_saga_by_id(saga_id, db)

    return saga