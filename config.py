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
    port: str = os.getenv("AUTH_PORT")

class ProfileURL(BaseModel):
    host: str = os.getenv("PROFILE_HOST", "arch.homework")
    path: str = os.getenv("PROFILE_PATH")
    register_endpoint: str = os.getenv("PROFILE_CREATE_ENDPOINT", "users")
    get_endpoint: str = os.getenv("PROFILE_GET_ENDPOINT", "users")
    upd_endpoint: str = os.getenv("PROFILE_UPD_ENDPOINT", "users")
    port: str = os.getenv("PROFILE_PORT")

class AuthJWT(BaseModel):
    public_key_path: Path =  BASE_DIR /os.getenv("JWT_PUBLIC_PATH", "./etc/keys/jwt-public.pem")
    algorithm: str = os.getenv("JWT_ALGORITH", "RS256")

class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    auth_url: AuthURL = AuthURL()
    prof_url: ProfileURL = ProfileURL()

settings = Settings()