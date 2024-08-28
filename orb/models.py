from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4
from asyncpg import Pool
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

class Media(BaseModel):
    mid: UUID = uuid4()
    pid: UUID                # Post ID (Many-to-one relationship with Post)
    url: Optional[str]     # An array of urls
    type: str
    format: str
    date: datetime = datetime.now()


class MediaRepository(ABC):

    @abstractmethod
    async def create_table(self, pool: Pool) -> None:
        """ Create media table """

    @abstractmethod
    async def store_media(self, pool: Pool, media: Media) -> Media:
        """ Store media item in database """

    @abstractmethod
    async def fetch_media(self, pool: Pool, mediaID: UUID) -> Media:
        """ Fetch media item from database """

    @abstractmethod
    async def fetch_media_by_uid(self, pool: Pool, uid: UUID) -> List[Media]:
        """ Fetch media items by user ID """

    @abstractmethod
    async def fetch_media_by_post(self, pool: Pool, postid: UUID) -> List[Media]:
        """ Fetch media by associated post """

    @abstractmethod
    async def delete_media(self, pool: Pool, mediaID: UUID) -> bool:
        """ Delete media with associated ID """



