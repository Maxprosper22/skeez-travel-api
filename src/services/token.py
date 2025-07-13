from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime, timedelta
import jwt
from asyncpg.pool import Pool

from src.models.token import Token, TokenType

class TokenService:
    @classmethod
    async def create_table(cls, pool: Pool) -> None:
        async with pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS tokens (
                    token_id UUID PRIMARY KEY,
                    account_id UUID REFERENCES accounts ON UPDATE CASCADE ON DELETE RESTRICT,
                    valid BOOLEAN NOT NULL,
                    issue_date TIMESTAMP NOT NULL,
                    expiry TIMESTAMP NOT NULL,
                    token_type TEXT NOT NULL,
                    signature TEXT UNIQUE NOT NULL
                )
            """)

    @classmethod
    async def generate_token(cls, pool: Pool, token: Token, key: str) -> str:
        """
            Generates auth token from a token Model.

            Arguments:
                self: AuthTokenManager class instance.
                pool: Database connection pool object.
                token: Instance of the Token class.
                key: Private key string. For signing JWT.

            Return -> str: JWT string
        """

        try:
            payload = {
                'sub': token.account_id,
                'iat': token.issue_date,
                'exp': token.expiry,
                'type': token.token_type
            }
            token_str = jwt.encode(payload, key, algorithm="ES256K")
            # Functionality to store token moved up

            return token_str

        except Exception as e:
            raise e

    @classmethod
    async def store_token(cls, pool: Pool, token: Token):
        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO tokens (
                    token_id,
                    account_id,
                    valid,
                    issue_date,
                    expiry,
                    token_type,
                    signature
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            """, token.token_id, token.account_id, token.valid, token.issue_date, token.expiry, token.signature)

    @classmethod
    async def fetch_token_by_id(cls, pool: Pool, account_id: UUID, signature: str) -> Optional[Token]:
        async with pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT * FROM tokens WHERE account_id=$1 AND signature=$2
            """, account_id, signature)
            if row:
                return Token(**dict(row))
            return None

    # async def fetch_by_signature

    @classmethod
    async def invalidate_token(cls, pool: Pool, account_id: UUID, signature: str):
        async with pool.acquire() as conn:
            await conn.execute("""
                UPDATE tokens SET valid=false WHERE account_id=$1 AND signature=$2
            """, account_id, signature)

    @classmethod
    async def check_token(cls, pool: Pool, token: str) -> Optional[Token]:
        """
            Check the validity of a token.
        """
        try:

            async with pool.acquire() as conn:
                row = await conn.fetchrow("""
                    SELECT * FROM tokens WHERE signature=$1
                """, token)
            if row:
                expiration = row['expiry']
                if expiration < datetime.now():
                    await cls.invalidate_token(pool, row['token_id'])
                    return None
                return Token(**dict(row))
            return None
        except Exception as e:
            raise e


