from pydantic import BaseModel
from uuid import UUID

class Ticket(BaseModel):
    trip_id: UUID
    account_id: UUID
