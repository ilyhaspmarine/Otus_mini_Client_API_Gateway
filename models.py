from pydantic import BaseModel, EmailStr, Field

class TokenInfo(BaseModel):
    access_token: str
    token_type: str

class UserName(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)

class Password(BaseModel):
    password: str = Field(..., min_length=3, max_length=50)

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