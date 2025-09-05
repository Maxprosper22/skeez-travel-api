from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime, timedelta
import jwt, pprint
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
                'sub': token.account_id.hex,
                'iat': token.issue_date,
                'exp': token.expiry,
                'type': token.token_type.value
            }
            token_str = jwt.encode(payload, key, algorithm="ES256K")
            # Functionality to store token moved up

            return token_str

        except Exception as e:
            raise e

    @classmethod
    async def store_token(cls, pool: Pool, token: Token):
        # pprint.pp(token.token_type)
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
            """, token.token_id, token.account_id, token.valid, token.issue_date, token.expiry, token.token_type.value, token.signature)

    @classmethod
    async def fetch_token(cls, pool: Pool, accountid: UUID = None, tokenid = None, signature: str = None) -> Optional[Token]:
        """ Retrieve token from database """
        try:
            if tokenid:
                async with pool.acquire() as conn:
                    row = await conn.fetchrow("""
                        SELECT * FROM tokens WHERE token_id=$1
                    """, token_id, signature)

                if not row:
                    return None

            elif signature:
                async with pool.acquire() as conn:
                    row = await conn.fetchrow("""
                        SELECT * FROM tokens WHERE signature=$1
                    """, signature)

                if not row:
                    return None

            token_dict = dict(row)
            return Token(
                token_id = token_dict['token_id'],
                account_id = token_dict['account_id'],
                valid = token_dict['valid'],
                issue_date = token_dict['issue_date'],
                expiry = token_dict['expiry'],
                token_type = token_dict['token_type'],
                signature = token_dict['signature']
            )

        except Exception as e:
            raise e

    @classmethod
    async def invalidate_token(cls, pool: Pool, tokenid: UUID = None, signature: str = None):
        try:
            if tokenid:
                async with pool.acquire() as conn:
                    await conn.execute("""
                        UPDATE tokens SET valid=false WHERE token_id=$1
                    """, token_id)
                token = await cls.fetch_token(pool, tokenid=tokenid)
            elif signature:
                async with pool.acquire() as conn:
                    await conn.execute("""
                        UPDATE tokens SET valid=false WHERE signature=$1
                    """, signature)
                token = await cls.fetch_token(pool, signature=signature)

            if not token:
                return None

            return token

        except Exception as e:
            raise e

    @classmethod
    async def validate(cls, pool: Pool, tokenid: UUID = None, signature: str = None) -> Optional[Token]:
        """
            Check the validity of a token.
        """
        try:
            if tokenid:
                token = await cls.fetch_token(pool, tokenid=tokenid)
                if not token:
                    return None

            elif signature:
                token = await cls.fetch_token(pool=pool, signature=signature)
                if not token:
                    return None
                
            expiration = token.expiry

            if expiration >= datetime.now() or token.valid == False:
                token = await cls.invalidate_token(pool, token.token_id)
                return None

            return token

        except Exception as e:
            raise e


