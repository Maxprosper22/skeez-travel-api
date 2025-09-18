from typing import Optional
from pydantic import BaseModel, Field, EmailStr, SecretStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from uuid import UUID, uuid4
from asyncpg import Pool
from datetime import datetime

from .admin import Admin
from .trip import Trip, TripStatus

class Account(BaseModel):
    account_id: UUID = Field(default_factory=lambda _: uuid4())
    email: EmailStr
    phone_number: PhoneNumber
    password: str
    firstname: str
    lastname: str
    othername: Optional[str] = None
    join_date: datetime = Field(default_factory=lambda _: datetime.now().replace(second=0, microsecond=0))
    is_admin: bool = False
    admin: Optional[Admin] = None
    trips: Optional[Trip] = None
