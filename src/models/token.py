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
    token_id: UUID = Field(default_factory=uuid4())
    account_id: UUID
    valid: bool
    issue_date: datetime = Field(default_factory=datetime.now())
    expiry: datetime = Field(default_factory=datetime.now() + timedelta(minutes=2))
    token_type: TokenType
    signature: Optional[str]



