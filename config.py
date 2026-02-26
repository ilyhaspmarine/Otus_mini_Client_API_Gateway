from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import os

BASE_DIR = Path(__file__).parent

class AuthURL(BaseModel):
    host: str = os.getenv("AUTH_HOST", "arch.homework")
    path: str = os.getenv("AUTH_PATH")
    login_endpoint: str = os.getenv("AUTH_LOGIN_ENDPOINT", "login")
    register_endpoint: str = os.getenv("AUTH_REG_ENDPOINT", "register")
    unregister_endpoint: str = os.getenv("AUTH_UNREG_ENDPOINT", "delete")
    port: str = os.getenv("AUTH_PORT")

class ProfileURL(BaseModel):
    host: str = os.getenv("PROFILE_HOST", "arch.homework")
    path: str = os.getenv("PROFILE_PATH")
    register_endpoint: str = os.getenv("PROFILE_CREATE_ENDPOINT", "users")
    get_endpoint: str = os.getenv("PROFILE_GET_ENDPOINT", "users")
    upd_endpoint: str = os.getenv("PROFILE_UPD_ENDPOINT", "users")
    del_endpoint: str = os.getenv("PROFILE_DEL_ENDPOINT", "users")
    port: str = os.getenv("PROFILE_PORT")

class BillingURL(BaseModel):
    host: str = os.getenv("BILLING_HOST", "arch.homework")
    path: str = os.getenv("BILLING_PATH")
    register_endpoint: str = os.getenv("BILLING_CREATE_ENDPOINT", "register")
    wallet_get_endpoint: str = os.getenv("BILLING_WALLET_GET_ENDPOINT", "wallet")
    transaction_endpoint: str = os.getenv("BILLING_TRANSACTION_ENDPOINT", "transaction")
    storno_endpoint: str = os.getenv("BILLING_STORNO_ENDPOINT", "transaction/storno")
    port: str = os.getenv("BILLING_PORT")

class OrdersURL(BaseModel):
    host: str = os.getenv("ORDERS_HOST", "arch.homework")
    path: str = os.getenv("ORDERS_PATH")
    create_endpoint: str = os.getenv("ORDERS_CREATE_ENDPOINT", "orders")
    event_endpoint: str = os.getenv("ORDERS_EVENT_ENDPOINT", "orders")
    get_by_id_endpoint: str = os.getenv("ORDERS_GET_BY_ID_ENDPOINT", "orders/id")
    get_by_user_endpoint: str = os.getenv("ORDERS_GET_BY_USER_ENDPOINT", "orders/user")
    port: str = os.getenv("ORDERS_PORT")


class NotificationUrl(BaseModel):
    host: str = os.getenv("NOTIFICATIONS_HOST", "arch.homework")
    path: str = os.getenv("NOTIFICATIONS_PATH")
    port: str = os.getenv("NOTIFICATIONS_PORT")
    get_by_order_id_endpoint: str = os.getenv("NOTIFICATIONS_GET_BY_ORDER_ID_ENDPOINT", "order")

class WarehouseURL(BaseModel):
    host: str = os.getenv("WAREHOUSE_HOST", "arch.homework")
    path: str = os.getenv("WAREHOUSE_PATH")
    good_create_endpoint: str = os.getenv("WAREHOUSE_GOOD_CREATE_ENDPOINT", "goods")
    stock_create_endpoint: str = os.getenv("WAREHOUSE_STOCK_CREATE_ENDPOINT", "stocks")
    stock_get_endpoint: str = os.getenv("WAREHOUSE_STOCK_GET_ENDPOINT", "stocks")
    reserve_create_endpoint: str = os.getenv("WAREHOUSE_RESERVE_CREATE_ENDPOINT", "reservations")
    reserve_get_endpoint: str = os.getenv("WAREHOUSE_RESERVE_GET_ENDPOINT", "reservations/order")
    reserve_cancel_endpoint: str = os.getenv("WAREHOUSE_RESERVE_CANCEL_ENDPOINT", "reservations/order/cancel")
    port: str = os.getenv("WAREHOUSE_PORT")

class DeliveryURL(BaseModel):
    host: str = os.getenv("DELIVERY_HOST", "arch.homework")
    path: str = os.getenv("DELIVERY_PATH")
    port: str = os.getenv("DELIVERY_PORT")
    courier_create_endpoint: str = os.getenv("DELIVERY_COURIER_CREATE_ENDPOINT", "couriers")
    delivery_create_endpoint: str = os.getenv("DELIVERY_CREATE_ENDPOINT", "deliveries")
    delivery_get_endpoint: str = os.getenv("DELIVERY_GET_ENDPOINT", "deliveries")
    delivery_cancel_endpoint: str = os.getenv("DELIVERY_CANCEL_ENDPOINT", "deliveries/cancel")

class AuthJWT(BaseModel):
    public_key_path: Path =  BASE_DIR /os.getenv("JWT_PUBLIC_PATH", "./etc/keys/jwt-public.pem")
    algorithm: str = os.getenv("JWT_ALGORITH", "RS256")


class DbSettings(BaseModel):
    driver: str = "postgresql+" + os.getenv("DB_DRIVER_ASYNC", "asyncpg")
    username: str = os.getenv("DB_USER", "username")
    password: str = os.getenv("DB_PASSWORD", "password")
    host: str = os.getenv("DB_HOST", "host.docker.internal")
    port: str = os.getenv("DB_PORT", "5432")
    database: str = os.getenv("DB_NAME", "saga")

class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    auth_url: AuthURL = AuthURL()
    prof_url: ProfileURL = ProfileURL()
    bill_url: BillingURL = BillingURL()
    order_url: OrdersURL = OrdersURL()
    notif_url: NotificationUrl = NotificationUrl()
    deliv_url: DeliveryURL = DeliveryURL()
    wareh_url: WarehouseURL = WarehouseURL()
    db: DbSettings = DbSettings()

settings = Settings()