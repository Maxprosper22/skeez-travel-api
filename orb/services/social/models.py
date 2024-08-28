from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4
from asyncpg import Pool
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

class Post(BaseModel):
    pid: UUID = uuid4()
    uid: UUID
    content: str = ''
    media: Optional[Media]    # An array of urls ()
    quote: Optional[UUID]   # Quoted post ID (One-to-one relationship)
    date: datetime = datetime.now()

class PostRepository(ABC):

    @abstractmethod
    async def create_table(self, pool: Pool) -> None:
        """ Create post table in database """

    @abstractmethod
    async def store_post(self, pool: Pool, post: Post) -> Post:
        """ Store new post in database """

    @abstractmethod
    async def fetch_post(self, pool: Pool, postid: UUID) -> Post:
        """ Fetch post with given ID from database """

    @abstractmethod
    async def fetch_posts(self, pool: Pool, uid: UUID) -> Optional[Post]:
        """ Fetch all users posts """

    @abstractmethod
    async def delete_post(self, pool: Pool, postid: UUID) -> bool:
        """ Delete post with given ID from the database """

    @abstractmethod
    async def fetch_feed(self, pool: Pool, uid: UUID) -> List[Post]:
        """ Fetch a posts for user's feed """

class PostDBRepository(PostRepository):

    async def create_table(self, pool: Pool) -> None:
        async with pool.acquire() as conn:
            await conn.execute("""
                               CREATE TABLE IF NOT EXISTS posts (
                                   pid UUID PRIMARY KEY,
                                   uid UUID REFERENCES users ON UPDATE CASCADE ON DELETE CASCADE,
                                   )
                               """)
        return 
