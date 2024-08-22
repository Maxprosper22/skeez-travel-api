from typing import Optional
from asyncpg import Pool
from pydantic import BaseModel
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

class Token(BaseModel):
    tkid: UUID = uuid4()
    uid: UUID
    type: str = 'auth' # 'auth', 'reset'
    state: str # 'active', 'expired'
    date: datetime = datetime.now()
    expiry: datetime = datetime.now() + timedelta(minutes=10)


class Reset(BaseModel):
    rsid: UUID = uuid4()
    uid: UUID
    code: int
    date: datetime = datetime.now()

class TokenRepository(ABC):

    @abstractmethod
    async def create_table(self, pool: Pool) -> None:
        """ Create token table """

    @abstractmethod
    async def store_token(self, pool: Pool, token: Token) -> Optional[Token]:
        """ Store generated token in token store

        Parameters:
            pool: A database connection pool
            token: Token class instance
            signature: JWT signature of token

        Returns:
            None
        """

    @abstractmethod
    async def invalidate_token(self, pool: Pool, tokenid: UUID) -> bool:
        """ Invalidates token with the specified id

        Parameters:
            pool: A databse connection pool
            tokenid: ID of token to be invalidated

        Returns:
            bool: Status of operation
        """

    @abstractmethod
    async def fetch_token(self, pool: Pool, tokenid: UUID) -> Optional[Token]:
        """ Fetch token matching given ID from database
        Arguments:
            pool: Database connection pool
            tokenid: ID of token to fetch
        Returns:
            Token: An instance of the Token class
        """

    @abstractmethod
    async def check_token(self, pool: Pool, token: Token) -> Optional[Token]:
        """ Checks validity of token 
        Parameters:
            pool: Database connection pool
            token: Token instance
        Returns:
            Optional token instance
        """


class PGTokenRepository(TokenRepository):

    async def create_table(self, pool: Pool) -> None:
        try:
            async with pool.acquire() as conn:
                await conn.execute("""
                                   CREATE TABLE IF NOT EXISTS tokens (
                                       tkid UUID PRIMARY KEY,
                                       uid UUID REFERENCES users ON UPDATE CASCADE DELETE RESTRICT,
                                       type VARCHAR(10) NOT NULL,
                                       state VARCHAR(10) NOT NULL,
                                       date TIMESTAMP NOT NULL,
                                       expiry TIMESTAMP NOT NULL,
                                       )
                                   """)
        except Exception as e:
            print(f"An error occurred when create token table: [Error] {e}")

            raise e

    async def store_token(self, pool: Pool, token: Token) -> Optional[Token]:
        """"""
        try:
            async with pool.acquire() as conn:
                token_record = await conn.fetchrow(f"SELECT * FROM tokens WHERE tkid={token.tkid} and uid={token.uid}")

                if token_record:
                    return None

                await conn.execute(f"INSERT INTO tokens (tkid, uid, type, state, date, expiry) VALUES ('{token.tkid}', '{token.uid}', '{token.type}', '{token.state}', '{token.date}', '{token.expiry}')")

                return token
        except Exception as e:
            print(f"(Database Operation) [Error] An error occured when storing token: {e}.")
            raise e

    async def invalidate_token(self, pool: Pool, tokenid: UUID) -> bool:
        try:
            async with pool.acquire() as conn:
                token = await conn.fetchrow(f"SELECT * FROM tokens WHERE tkid={tokenid}")

                if not token:
                    return False

                await conn.execute("UPDATE tokens SET state='expired' WHERE tkid={tokenid}")
                return True
        except Exception as e:
            print(f"(Database Operation) [Error] An error occurrde when handling token invalidation: {e}")
            raise e

    async def fetch_token(self, pool: Pool, tokenid: UUID) -> Optional[Token]:
        try:
            async with pool.acquire() as conn:
                row = await conn.fetchrow("""SELECT * FROM tokens WHERE tkid=$1""", tokenid)
            if not row:
                return None

            token = Token(**dict(row))
            return token
        except Exception as e:
            print(e)

    async def check_token(self, pool: Pool, token: Token) -> Optional[Token | None]:
        try:
            async with pool.acquire() as conn:
                row = await conn.fetchrow("""
                                          SELECT * FROM tokens WHERE tkid=$1 and uid=$2
                                          """, token.tkid, token.uid)
            
            if row:
                expiration = row['expiration']
                if expiration < datetime.now():
                    await self.invalidate_token(pool, row['tkid'])
                    return None
                return Token(**dict(row))
            return None
        except Exception as e:
            print(f'An exception occurred! {e}')
