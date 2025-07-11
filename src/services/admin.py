from asyncpg import Pool
from uuid import UUID
from typing import Optional

from src.models.admin import Admin, AdminRole

class AdminService:
    @classmethod
    async def create_table(cls, pool: Pool) -> None:
        """ Creates a new admin tabke if none exists """

        try:
            async with pool.acquire() as conn:
                await conn.execute("""CREATE TABLE IF NOT EXISTS admin (
                    admin_id UUID PRIMARY KEY,
                    account_id UUID REFERENCES accounts (account_id) ON DELETE RESTRICT ON UPDATE CASCADE,
                    role TEXT NOT NULL,
                    date TIMESTAMP NOT NULL
                )""")
        except Exception as e:
            raise e

    @classmethod
    async def create_admin(cls, pool: Pool, admin: Admin) -> Optional[Admin]:
        """ Creates a new admin instance """
