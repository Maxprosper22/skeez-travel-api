from asyncpg.connection import traceback
from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4
from asyncpg import Pool
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

from orb.views import post

class Post(BaseModel):
    pid: UUID = uuid4()
    uid: UUID
    content: str = ''
    media: Optional[List[UUID]]    # An array of urls ()
    quote: Optional[UUID]   # Quoted post ID (One-to-one relationship)
    date: datetime = datetime.now()

class PostRepository(ABC):

    @abstractmethod
    async def create_table(self, pool: Pool) -> None:
        """ Create post table in database """

    @abstractmethod
    async def store_post(self, pool: Pool, post: Post) -> Optional[Post]:
        """ Store new post in database """

    @abstractmethod
    async def fetch_post(self, pool: Pool, postid: UUID) -> Optional[Post]:
        """ Fetch post with given ID from database """

    @abstractmethod
    async def fetch_posts(self, pool: Pool, uid: UUID) -> Optional[List[Post]]:
        """ Fetch all users posts """

    @abstractmethod
    async def fetch_timeline(self, pool: Pool, uid: UUID, following: Optional[List[UUID]]) -> Optional[List[Post]]:
        """ Fetch user timeline """

    @abstractmethod
    async def delete_post(self, pool: Pool, postid: UUID) -> bool:
        """ Delete post with given ID from the database """

    @abstractmethod
    async def fetch_feed(self, pool: Pool, uid: UUID) -> Optional[List[Post]]:
        """ Fetch a posts for user's feed """

class PostDBRepository(PostRepository):

    async def create_table(self, pool: Pool) -> None:
        """ Create posts table """
        try:
            async with pool.acquire() as conn:
                await conn.execute("""
                                   CREATE TABLE IF NOT EXISTS posts (
                                       pid UUID PRIMARY KEY,
                                       uid UUID NOT NULL,
                                       content TEXT,
                                       media TEXT[],
                                       quote UUID,
                                       date TIMESTAMP NOT NULL
                                    )
                                """) 
        except Exception as e:
            print(traceback.format_exc(e))

    async def store_post(self, pool: Pool, post: Post) -> Optional[Post]:
        """ Store post in the database """
        try:
            async with pool.acquire() as conn:
                await conn.execute("INSERT INTO posts (pid, uid, content, media, quote, date) VALUES ($1, $2, $3, $4, $5, $6)", **post)

                row = conn.fetchrow("SELECT * FROM posts WHERE pid=$1", post.pid)

            if not row:
                return None
            
            post_dict = dict(row)
            post = Post(**post_dict)

            return post

        except Exception as e:
            print(traceback.format_exc(e))

    async def fetch_post(self, pool: Pool, postid: UUID) -> Optional[Post]:
        """ Fetch post with given ID """
        try:
            async with pool.acquire() as conn:
                row = await conn.fetchrow("SELECT * FROM ROW WHERE pid=$1", postid)

            if not row:
                return None

            post_dict = dict(row)
            post = Post(**post_dict)

            return post
        except Exception as e:
            print(traceback.format_exc(e))

    async def fetch_posts(self, pool: Pool, uid: UUID) -> Optional[Post]:
        """ Fetch user posts """
        try:
            async with pool.acquire() as conn:
                rows = await conn.fetchrows("SELECT * FROM posts WHERE uid=$1", uid)

            if not rows:
                return None

            post_array = [dict(row) for row in rows]
            posts = [Post(**post) for post in post_array]

            return posts

        except Exception as e:
            print(traceback.format_exc(e))

