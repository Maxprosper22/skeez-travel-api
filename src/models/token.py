from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime, timedelta
from enum import Enum

class TokenType(Enum):
    AUTH = "auth"
    RESET = "reset"

class Token(BaseModel):
    token_id: UUID = Field(default_factory=lambda _: uuid4())
    account_id: UUID
    valid: bool
    issue_date: datetime = Field(default_factory=lambda _: datetime.now().replace(second=0, microsecond=0))
    expiry: datetime = Field(default_factory=lambda _: datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=2))
    token_type: TokenType
    signature: Optional[str] = None



