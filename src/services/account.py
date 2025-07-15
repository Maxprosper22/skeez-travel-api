from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from uuid import UUID, uuid4
from asyncpg import Pool
from datetime import datetime

from src.models.account import Account
from src.models.admin import Admin
import pprint

class AccountService(BaseModel):
    accounts: Optional[list[Account]] = []
    
    @classmethod
    async def create_table(cls, pool: Pool) -> None:
        """ Creates account table if it does not exist """
        try:
            async with pool.acquire() as conn:
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS accounts ( 
                        account_id UUID PRIMARY KEY,
                        email TEXT UNIQUE NOT NULL,
                        phone_number VARCHAR(30) NOT NULL,
                        password TEXT NOT NULL,
                        firstname TEXT NOT NULL,
                        lastname TEXT NOT NULL,
                        othername TEXT,
                        join_date TIMESTAMP NOT NULL,
                        is_admin BOOLEAN NOT NULL
                    )
                """)

        except Exception as e:
            raise e

    @classmethod
    async def create_account(cls, pool: Pool, account: Account) -> Optional[Account]:
        """ Create new account """
        
        try:
            async with pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO accounts (
                        account_id, email, phone_number, password, firstname, lastname, othername, join_date, is_admin
                    ) VALUES (
                        $1, $2, $3, $4, $5, $6, $7, $8, $9
                    ) RETURNING *""",
                    account.account_id,
                    account.email,
                    account.phone_number,
                    account.password,
                    account.firstname,
                    account.lastname,
                    account.othername,
                    account.join_date,
                    account.is_admin
                )
    
            return True

        except Exception as e:
            pprint.pp(f"An error occurred during account creation: {e}")
            return False

    @classmethod
    async def fetch_user(cls, pool: Pool, accountid: UUID) -> Optional[Account]:
        """ Fetch user for self.accounts """
    
        match cls.accounts:
            case [Account(account_id=account_id) as account]:
                print(account)

                return account

            case _:
                async with pool.acquire() as conn:
                    account_record = await conn.execute("""
                        SELECT * FROM accounts INNER JOIN accounts acct ON admin adm WHERE account_id = $1
                    """, accountid)

                if not account_record:
                    return None
                
                account_dict = dict(account_record)
                # accout_dict.pop("password")

                account = Account(
                    account_id = account_dict["account_id"],
                    email = account_dict["email"],
                    phone_number = account_dict["phone_number"],
                    passwordb= account_dict["password"],
                    firstname = account_dict["firstname"],
                    lastname = account_dict["lastname"],
                    othername = account_dict["othername"],
                    join_date = account_dict["join_date"],
                    is_admin = account_dict["is_admin"],
                    admin = Admin(
                        admin_id = account_dict["admin_id"],
                        account_id = account_dict["account_id"],
                        roles = account_dict["roles"],
                        date = account_dict["date"]
                    )
                )
        
                return account

    @classmethod
    async def populate_accounts(cls, pool: Pool):
        """ 
            Retrieve account data from database. Runs on server startup.
        """

        try:
            async with pool.acquire() as conn:
                account_records = await conn.fetch("""
                    SELECT * FROM accounts 
                    LEFT JOIN admin adm ON accounts.account_id = adm.account_id 
                    LEFT JOIN tickets tkt ON accounts.account_id = tkt.account_id
                """)

            print(f"Account records: {account_records}; type {type(account_records)}")
            
            if not account_records:
                return None

            accounts_dict = dict(account_records)
            pprint.pp(accounts_dict)
            for account_record in accounts_dict:
                account = Account(
                    account_id = account_dict["account_id"],
                    email = account_dict["email"],
                    phone_number = account_dict["phone_number"],
                    password = account_dict["password"],
                    firstname = account_dict["firstname"],
                    lastname = account_dict["lastname"],
                    othername = account_dict["othername"],
                    join_date = account_dict["join_date"],
                    is_admin = account_dict["is_admin"],
                    admin = Admin(
                        admin_id = accounts_dict["admin_id"],
                        account_id = accounts_dict["account_id"],
                        role = accounts_dict["role"],
                        date = accounts_dict["date"]
                    ),
                    trips=[Trip(trip_id=trip["trip_id"], destination=trip["destination"], capacity=trip["capacity"], status=trip["status"], date=trip["date"]) for trip in accounts_dict["trips"]]
                )
                cls.accounts.append(account)

            # return account_records

        except Exception as e:
            raise e
