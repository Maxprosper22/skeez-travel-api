from pydantic import BaseModel, EmailStr, Field, field_validator
from asyncpg import Pool
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from typing import Optional, List, Dict, TypeVar, Any
from enum import Enum

# from src.services import Publisher, Channel, SSESubscriber, SMSSubscriber, EmailSubscriber
from src.utils.slotlist import SlotList

class TripStatus(Enum):
    PENDING = "pending"        # Trip is waiting to beginning
    ACTIVE = "active"          # Trip is underway
    COMPLETE = "complete"      # Trip is done
    CANCELLED = "cancelled"    # Trip is/was cancelled

class DestinationType(Enum):
    WARRI = {'destination': 'Warri', 'price': '5000'}
    PORT_HARCOURT = {'destination': 'Port Harcourt', 'price': '4500'}

class Destination(BaseModel):
    destination_id: UUID = Field(default_factory=lambda _: uuid4())
    name: str
    price: float

class Trip(BaseModel):
    trip_id: UUID = Field(default_factory=lambda: uuid4())
    destination: Destination
    capacity: int = 10
    slots: Optional[SlotList[Dict]] = []  # A list of passengers
    status: TripStatus = Field(default=TripStatus.PENDING)
    date: datetime = Field(default_factory= lambda _: datetime.now().replace(second=0, microsecond=0))
    # sms_channel: Channel
    # email_channel: Channel
    # sse_channel: Channel

    @field_validator("slots", mode="before")
    def initialize_slots(cls, slots: Any, values: Any) -> SlotList[Dict]:
        # Get capacity from values
        # print("SlotList values: ", values.__dir__())
        # print("SlotList values: ", values.data)
        capacity = values.data.get("capacity")
        if capacity is None:
            raise ValueError("Capacity must be available to initialize slots")
        # Handle None or empty fruitsf
        if slots is None:
            return SlotList(max_length=capacity)

        # Convert input to FixedLengthList if it's a list
        if isinstance(slots, list):
            return SlotList(slots=slots, max_length=capacity)

        raise ValueError("Slots must be a list or None")

    def __lt__(self, other):
        if not isinstance(other, Trip):
            return NotImplemented
        return self.trip_id < other.trip_id  # Compare based on tripid

    class Config:
        # Allow custom types like FixedLengthList
        arbitrary_types_allowed = True
