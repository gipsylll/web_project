from pydantic import BaseModel, EmailStr
from typing import Optional, List
from decimal import Decimal

# ### Общие схемы ###

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    is_admin: bool = False

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    full_name: Optional[str]
    password: Optional[str]

class UserOut(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True


class AccountOut(BaseModel):
    id: int
    balance: Decimal

    class Config:
        orm_mode = True


class PaymentOut(BaseModel):
    id: int
    transaction_id: str
    amount: Decimal

    class Config:
        orm_mode = True


# ### Схемы для авторизации ###

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int
    is_admin: bool


# ### Схемы для входа (login) ###

class LoginSchema(BaseModel):
    email: EmailStr
    password: str


# ### Схемы для вебхука платежей ###

class PaymentWebhook(BaseModel):
    transaction_id: str
    account_id: int
    user_id: int
    amount: Decimal
    signature: str