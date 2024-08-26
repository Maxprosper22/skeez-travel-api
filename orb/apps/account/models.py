from pydantic import BaseModel, EmailStr
from asyncpg import Pool
from uuid import UUID, uuid4
from abc import ABC, abstractmethod
from typing import Optional, List

class User(BaseModel):
    uid: UUID = uuid4()
    email: EmailStr
    username: str
    firstname: str
    lastname: str
    password: str

class UserRepository(ABC):

    @abstractmethod
    async def create_table(self, pool: Pool) -> None:
        """ Create user table in database """

    @abstractmethod
    async def create_user(self, pool: Pool, user: User) -> User:
        """ Create new user account 

        Parameters:
            pool: Database connection pool
            user: User model instance

        Returns:
            user: A new instance of the User class
        """

    @abstractmethod
    async def delete_user(self, pool: Pool, uid: UUID) -> bool:
        """ Delete user account associated with specified ID

        Parameters:
            pool: A database connecton pool
            uid: User's associated UUID str

        Returns:
            bool: Boolean representation of the operation's result
        """

    @abstractmethod
    async def validate_user(self, pool: Pool, password: str, email: EmailStr, username: str) -> Optional[User]:
        """ Validate user credentials

        Parameters:
            pool: A database connection pool
            password: User's password
            email: Email associated with user's account
            username: Username associated with account

        Returns:
            Optional[User]: An instance of the User class if account exists
        """

    @abstractmethod
    async def fetch_user_by_email(self, pool: Pool, email: EmailStr) -> Optional[dict]:
        """ Fetch user by email

        Parameters:
            pool: Database connection pool
            email: User email address

        Returns:
            Optional[user]: An instance of the User model class
        """

    @abstractmethod
    async def fetch_user_by_uid(self, pool: Pool, uid: UUID) -> Optional[User]:
        """ Fetch user by associated ID

        Parameters:
            pool: Database connection pool
            uid: User's ID (a UUID str)

        Returns:
            Optional[User]: An instance of the User class if user exists
        """

    @abstractmethod
    async def fetch_all_users(self, pool: Pool) -> List[User]:
        """ Fetch all users in database

        Parameters:
            pool: A database connection pool

        Returns:
            LIst[User]: A list of users on the database
        """


