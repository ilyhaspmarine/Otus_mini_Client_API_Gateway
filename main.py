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
    NotificationReturn
)
from fastapi.security import OAuth2PasswordRequestForm
import utils
from uuid import UUID
from typing import List

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

@app.post("/orders", summary = 'Create order', tags = ['Orders'], response_model = OrderReturn, status_code = status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    token_payload: dict = Depends(utils.get_current_token_payload)
):
    order = await utils.process_new_order(order_data, token_payload)

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