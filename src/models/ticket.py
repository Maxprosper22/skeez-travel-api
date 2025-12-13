from pydantic import BaseModel
from uuid import UUID
from typing import Dict
from enum import Enum


class TicketStatus(Enum):
    CANCELLED = 'cancelled'
    ACTIVE = 'active'
    COMPLETE = 'complete'


class Ticket(BaseModel):
    trip_id: UUID
    account_id: UUID
    status: TicketStatus
    data: Dict
