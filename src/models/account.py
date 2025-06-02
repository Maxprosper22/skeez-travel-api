from asyncpg.connection import traceback
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from asyncpg import Pool
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

# from src.views import post

class Account(BaseModel):
    uid: UUID = Field(default_factory=lambda: uuid4())
    email: EmailStr
    firstname = str
    lastname = str
    username: str = ''
    password: str Field(exclude=True)
    date: datetime = datetime.now()

class AccountManager:

    async def create_table(self, pool: Pool) -> None:
        """ Create accounts table """
        try:
            async with pool.acquire() as conn:
                await conn.execute("""
                                   CREATE TABLE IF NOT EXISTS accounts (
                                       uid UUID PRIMARY JEY,
                                       email TEXT UNIQUE NOT NULL,
                                       firstname TEXT NOT NULL,
                                       lastname TEXT NOT NULL,
                                       username TEXT UNIQUE,
                                       password TEXT NOT NULL,
                                       date TIMESTAMP NOT NULL
                                    )
                                """) 
        except Exception as e:
            print(traceback.format_exc(e))
            raise e

    async def create(self, pool: Pool, account: Account) -> Optional[Account]:
        """ Create and store new account in the database """
        try:
            async with pool.acquire() as conn:
                await conn.execute("INSERT INTO accounts (uid, email, firstname, lastname, username, password, date) VALUES ($1, $2, $3, $4, $5, $6)", account.model_dump())

                row = conn.fetchrow("SELECT * FROM accounts WHERE uid=$1 OR email=$2", account.uid, account.email)

            if not row:
                return None
            
            post_dict = dict(row)
            post = Post(**post_dict)

            return post

        except Exception as e:
            print(traceback.format_exc(e))

    async def fetch(self, pool: Pool, uid: Optional[UUID], email: Optional[EmailStr], username: Optional[str]) -> Optional[Account]:
        """ Fetch account with given ID/email/username """
        try:
            async with pool.acquire() as conn:
                if email and uid == None and username == None:
                    accountData = await conn.fetchrow("SELECT * FROM accounts WHERE email=$1", email)
                elif uid and email == None and username == None:
                    accountData = await conn.fetchrow("SELECT * FROM accounts WHERE uid=$1", uid)
                elif username and email == None and uid == None:
                    accountData = await conn.fetchrow("SELECT * FROM accounts WHERE username=$1", username)
                else:
                    return "Please supply one of the following info tk proceed: User ID, E-mail or username"

            if not accountData:
                return None

            account_dict = dict(accountData)
            account = Account(**account_dict)

            return account

        except Exception as e:
            print(traceback.format_exc(e))

    async def fetch_all(self, pool: Pool, uid: UUID, email) -> Optional[List[Accounts]:
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






# class BaseAccountManager(ABC):
#
#     @abstractmethod
#     async def create_table(self, pool: Pool) -> None:
#         """ Create post table in database """
#
#     @abstractmethod
#     async def store_post(self, pool: Pool, post: Post) -> Optional[Post]:
#         """ Store new post in database """
#
#     @abstractmethod
#     async def fetch_post(self, pool: Pool, postid: UUID) -> Optional[Post]:
#         """ Fetch post with given ID from database """
#
#     @abstractmethod
#     async def fetch_posts(self, pool: Pool, uid: UUID) -> Optional[List[Post]]:
#         """ Fetch all users posts """
#
#     @abstractmethod
#     async def fetch_timeline(self, pool: Pool, uid: UUID, following: Optional[List[UUID]]) -> Optional[List[Post]]:
#         """ Fetch user timeline """
#
#     @abstractmethod
#     async def delete_post(self, pool: Pool, postid: UUID) -> bool:
#         """ Delete post with given ID from the database """
#
#     @abstractmethod
#     async def fetch_feed(self, pool: Pool, uid: UUID) -> Optional[List[Post]]:
#         """ Fetch a posts for user's feed """
#

