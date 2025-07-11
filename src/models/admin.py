from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from enum import Enum

class AdminRole(Enum):
    MOD = "mod"
    SUPERMOD = "supermod"

class Admin(BaseModel):
    admin_id: UUID = Field(default_factory=uuid4())
    account_id: UUID
    roles: AdminRole
    date: datetime = Field(default_factory=datetime.now())
