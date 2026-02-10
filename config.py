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
    port: str = os.getenv("BILLING_PORT")

class OrdersURL(BaseModel):
    host: str = os.getenv("ORDERS_HOST", "arch.homework")
    path: str = os.getenv("ORDERS_PATH")
    create_endpoint: str = os.getenv("ORDERS_CREATE_ENDPOINT", "orders")
    event_endpoint: str = os.getenv("ORDERS_EVENT_ENDPOINT", "orders")
    get_by_id_endpoint: str = os.getenv("ORDERS_GET_BY_ID_ENDPOINT", "orders/id")
    get_by_user_endpoint: str = os.getenv("ORDERS_GET_BY_USER_ENDPOINT", "orders/user")
    port: str = os.getenv("ORDERS_PORT")


class AuthJWT(BaseModel):
    public_key_path: Path =  BASE_DIR /os.getenv("JWT_PUBLIC_PATH", "./etc/keys/jwt-public.pem")
    algorithm: str = os.getenv("JWT_ALGORITH", "RS256")

class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    auth_url: AuthURL = AuthURL()
    prof_url: ProfileURL = ProfileURL()
    bill_url: BillingURL = BillingURL()
    order_url: OrdersURL = OrdersURL()

settings = Settings()