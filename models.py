from pydantic import BaseModel, EmailStr, Field, field_validator
from decimal import Decimal
from uuid import UUID 
from datetime import datetime
from typing import Optional
from typing import List

# _________________________________________________________
class TokenInfo(BaseModel):
    access_token: str
    token_type: str

class UserName(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)

class Password(BaseModel):
    password: str = Field(..., min_length=3, max_length=50)

class Amount(BaseModel):
    amount: Decimal = Field(..., max_digits = 15, decimal_places= 2)

class AmountStr(BaseModel):
    amount: str = Field(..., max_length = 17 )

class Price(BaseModel):
    price: Decimal = Field(..., max_digits = 15, decimal_places= 2)

class PriceStr(BaseModel):
    price: str = Field(..., max_length = 17 )

class ID(BaseModel):
    id: UUID

class IDStr(BaseModel):
    id: str

class Event(BaseModel):
    event: str

class CreatedAt(BaseModel):
    created_at: datetime

class Quantity(BaseModel):
    quantity: int
    
class GoodID(BaseModel):
    good_id: UUID

class GoodIDStr(BaseModel):
    good_id: str

class LastChanged(BaseModel):
    last_changed: datetime

class OrderID(BaseModel):
    order_id: UUID

class OrderIDStr(BaseModel):
    order_id: str
# _________________________________________________________


# _________________________________________________________
class OrderPosCreate(GoodID, Quantity, PriceStr):
    pass


class OrderCreateOrderService(UserName, PriceStr):
    pass


class OrderCreate(OrderCreateOrderService):
    address: str
    positions: List[OrderPosCreate] = []


class OrderUpdateEvent(IDStr, Event):
    payment_id: Optional[str] = None

class OrderReturn(ID, UserName, Price):
    status: str = Field()
    placed_at: datetime = Field()
    updated_at: datetime = Field() 
# _________________________________________________________


# _________________________________________________________
class ProfileBase(BaseModel):
    firstName: str = Field(..., min_length=1, max_length=100)
    lastName: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=12, max_length=12)

class Profile(ProfileBase, UserName):
    pass

class ProfileCreate(Profile):
    pass

class ProfileUpdate(ProfileBase):
    pass

class ProfileReturn(Profile):
    class Config:
        from_attributes = True
# _________________________________________________________


# _________________________________________________________
class AuthBase(UserName, Password):
    pass

class AuthCreate(AuthBase):
    pass

class AuthLogin(AuthBase):
    pass
# _________________________________________________________

# _________________________________________________________
class UserCreate(Profile, Password):
    pass
# _________________________________________________________


# _________________________________________________________
class WalletBase(UserName):
    pass

class WalletCreate(WalletBase):
    pass

class WalletReturn(WalletBase, Amount):
    pass

    class Config:
        from_attributes = True
# _________________________________________________________


# _________________________________________________________
class TransactionBase(UserName, Amount):
    pass

class TransactionCreate(UserName, AmountStr):
    pass

class TransactionReturn(TransactionBase):
    id: UUID = Field()

    class Config:
        from_attributes = True
# _________________________________________________________


# _________________________________________________________
class NotificationReturn(ID, UserName):
    order_id: UUID
    email: EmailStr
    sent_at: datetime
    text: str
    class Config:
        from_attributes = True
# _________________________________________________________


# _________________________________________________________
class GoodBase(PriceStr):
    name: str

class GoodCreate(GoodBase):
    pass

class GoodReturn(ID, GoodBase):
    pass
    class Config:
        from_attributes = True
# _________________________________________________________


# _________________________________________________________
class StockBase(Quantity, GoodIDStr):
    pass

class StockCreate(StockBase):
    pass


class StockReturn(ID, StockBase, CreatedAt, LastChanged):
    reserved: int
    available: int
    class Config:
        from_attributes = True
# _________________________________________________________


# _________________________________________________________
class ReservationPosCreate(GoodIDStr, Quantity):
    pass


class ReservationCreate(OrderIDStr):
    positions: List[ReservationPosCreate] = []


class ReservationHeadBase(ID, CreatedAt, OrderID, LastChanged):
    canceled: bool


class ReservationPositionBase(IDStr, Quantity):
    posno: int

    stock_id: UUID    


class ReservationReturn(ReservationHeadBase):
    positions: List[ReservationPositionBase]

    class Config:
        from_attributes = True
# _________________________________________________________



# _________________________________________________________
class CourierBase(BaseModel):
    first_name: str
    last_name: str  
    phone: str = Field(..., min_length=12, max_length=12)

class CourierCreate(CourierBase):
    pass

class CourierReturn(ID, CourierBase):
    pass
    class Config:
        from_attributes = True
# _________________________________________________________


# _________________________________________________________
class DeliveryBase(BaseModel):
    order_id: UUID
    address: str

class DeliveryCreate(DeliveryBase):
    pass

class DeliveryReturn(ID, DeliveryBase):
    courier_id: UUID
    courier_name: str
    status: str
    created_at: datetime
    last_changed: datetime
    class Config:
        from_attributes = True



class SagaReturn(ID):
    order_id: UUID | None = None
    order_cancelled: bool
    payment_id: UUID | None = None
    payment_cancelled: bool
    reservation_id: UUID | None = None
    reservation_cancelled: bool
    delivery_id: UUID | None = None
    delivery_cancelled: bool
    status: str
    last_updated: datetime


class OrderCreateStatusReturn(BaseModel):
    id: UUID | None = None
    error: str | None = None
    class Config:
        from_attributes = True