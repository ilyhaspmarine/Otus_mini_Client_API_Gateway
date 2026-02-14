from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from config import settings
import jwt
from models import (
    UserCreate,
    ProfileReturn,
    ProfileUpdate,
    WalletReturn,
    TransactionCreate,
    TransactionReturn,
    OrderCreate,
    OrderReturn,
    NotificationReturn
)
from services import AuthService, ProfileService, BillingService, OrderService, NotificationService
from saga import SagaRegister, SagaOrder
from uuid import UUID
from typing import List

http_bearer = HTTPBearer()


def check_response(
    response
):
    if not response.is_success:
        raise HTTPException(
            status_code=response.status_code, 
            detail=response.text
        )


def check_token_uname(
    uname: str,
    token_payload: dict
):
    if uname != token_payload.get("sub"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access forbidden",
        )


def profile_from_response(
    response
):
    json = response.json()    
    return ProfileReturn(
        username  = json.get("username"),
        email     = json.get("email"),
        phone     = json.get("phone"),
        firstName = json.get("firstName"),
        lastName  = json.get("lastName")
    )


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm]
    )
    return decoded


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    token = credentials.credentials
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error",
        )

    return payload


async def process_login(
    auth_data: OAuth2PasswordRequestForm
):
    auth_service = AuthService()

    response = await auth_service.login(auth_data)

    return response.json()


async def get_profile(
    req_uname: str,
    token_payload: dict
):
    # Если не совпадет - изнутри шибанет исключением 
    check_token_uname(req_uname, token_payload)

    profile_service = ProfileService()

    response = await profile_service.get_profile(req_uname)

    return profile_from_response(response)


async def update_profile(
    req_uname: str,
    profile_upd: ProfileUpdate,
    token_payload: dict
):
    # Если не совпадет - изнутри шибанет исключением 
    check_token_uname(req_uname, token_payload)

    profile_service = ProfileService()

    response = await profile_service.upd_profile(req_uname, profile_upd)
    
    return profile_from_response(response)


async def process_register(
    reg_data: UserCreate
):
    saga = SagaRegister()

    # Сага сама выкинет исключения при возникновении
    result = await saga.execute_saga(reg_data)

    return result


async def get_wallet(
    req_uname: str,
    token_payload: dict
):
    # Если не совпадет - изнутри шибанет исключением 
    check_token_uname(req_uname, token_payload)

    billing_service = BillingService()

    response = await billing_service.get_wallet(req_uname)

    json = response.json()

    return WalletReturn(
        username = json.get("username"),
        amount = json.get("amount")
    )


async def create_transaction(
    tr_data: TransactionCreate,
    token_payload: dict
):
    # Если не совпадет - изнутри шибанет исключением 
    check_token_uname(tr_data.username, token_payload)

    billing_service = BillingService()
    
    response = await billing_service.create_transaction(tr_data.username, tr_data.amount)

    json = response.json()

    return TransactionReturn(
        username = json.get("username"),
        amount   = json.get("amount"),
        id       = json.get("id")
    )


async def process_new_order(
    order_data: OrderCreate,
    token_payload: dict
):
    # Если не совпадет - изнутри шибанет исключением 
    check_token_uname(order_data.username, token_payload)

    saga = SagaOrder()

    result = await saga.execute_saga(order_data)

    return result


async def get_order_by_id(
    order_id: UUID,
    token_payload: dict
):
    order_service = OrderService()

    response = await order_service.get_order_by_id(order_id)

    json = response.json()

    order = OrderReturn(
        id = UUID(json.get('id')),
        username = json.get('username'),
        status = json.get('status'),
        price = json.get('price'),
        placed_at = json.get('placed_at'),
        updated_at = json.get('updated_at')
    )

    check_token_uname(order.username, token_payload)

    return order


async def get_orders_by_uname(
    req_uname: str,
    token_payload: dict
):
    check_token_uname(req_uname, token_payload)

    order_service = OrderService()

    response = await order_service.get_orders_by_uname(req_uname)

    data_list = response.json()

    orders: List[OrderReturn] = [OrderReturn.model_validate(item) for item in data_list]

    return orders


async def get_notifications_for_order(
    order_id: UUID,
    token_payload: dict
):
    order = await get_order_by_id(order_id, token_payload)

    notif_service = NotificationService()

    response = await notif_service.get_notifications_for_order_id(order_id)

    data_list = response.json()

    notifications: List[NotificationReturn] = [NotificationReturn.model_validate(item) for item in data_list]

    return notifications