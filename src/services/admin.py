from asyncpg import Pool
from uuid import UUID
from typing import Optional
import pprint

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

    @classmethod
    async def fetch(cls, pool: Pool, adminid: UUID = None, accountid: UUID = None) -> Optional[Admin]:
        """ Retrieves admin data. Requires either admin id or account id. If neither is available return an error """

        try:
            if adminid:
                async with pool.acquire() as conn:
                    admin_record = await conn.fetchrow("""SELECT * FROM admin WHERE admin_id=$1""", adminid)
                
                if not admin_record:
                        return None

                admin_data = dict(admin_record)
                pprint.pp(f'Admin data: {admin_data}')
                adminData = Admin(
                    admin_id=admin_data['admin_id'],
                    account_id=admin_data['account_id'],
                    role=admin_data['role'],
                    date=admin_data['date']
                )
                return adminData

            elif accountid:
                async with pool.acquire() as conn:
                    admin_record = await conn.fetchrow("""SELECT * FROM admin WHERE account_id=$1""", accountid)
                    
                if not admin_record:
                        return None

                admin_data = dict(admin_record)
                pprint.pp(f'Admin data: {admin_data}')
                adminData = Admin(
                    admin_id=admin_data['admin_id'],
                    account_id=admin_data['account_id'],
                    role=admin_data['role'],
                    date=admin_data['date']
                )
                return adminData

            else:
                return None

        except Exception as e:
            raise e
