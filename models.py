from pydantic import BaseModel, EmailStr, Field, field_validator
from decimal import Decimal
from uuid import UUID 


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



class AuthBase(UserName, Password):
    pass

class AuthCreate(AuthBase):
    pass

class AuthLogin(AuthBase):
    pass



class UserCreate(Profile, Password):
    pass



class WalletBase(UserName):
    pass

class WalletCreate(WalletBase):
    pass

class WalletReturn(WalletBase, Amount):
    pass

    class Config:
        from_attributes = True



class TransactionBase(UserName, Amount):
    pass

class TransactionCreate(UserName, AmountStr):
    pass

class TransactionReturn(TransactionBase):
    id: UUID = Field()

    class Config:
        from_attributes = True