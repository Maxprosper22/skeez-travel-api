from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class SessionToken(BaseModel):
    session_id: UUID = Field(default_factory=lambda _: uuid4())
    uid: UUID
    max_age: int

    expired: bool
    httponly: bool
