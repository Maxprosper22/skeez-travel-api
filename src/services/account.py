from typing import Optional, Dict
from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from uuid import UUID, uuid4
from asyncpg import Pool
from datetime import datetime

from src.models.account import Account
from src.models.admin import Admin

from .pubsub import Publisher, Channel, SMSSubscriber, EmailSubscriber, SSESubscriber
import pprint
import json

class AccountService:
    def __init__(self, pool: Pool, publisher: Publisher):
        self.accounts: Optional[Dict[str, Account]] = {}
        self.pool: Pool = pool
        self.publisher = Publisher
    
    async def create_table(self, pool: Pool) -> None:
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

    async def initialise(self, pool: Pool):
        """ 
            Retrieve account data from database. Runs on server startup.
        """
        try:
            records = await self.fetch(pool=pool)
            # pprint.pp(f"Account records: {records}; type {type(records)}")            
            if not records:
                return
            # accounts_array = [dict(account_record) for account_record in records]
            # pprint.pp(records)
            for account_dict in records:
                account = Account(
                    account_id = account_dict["account_id"],
                    email = account_dict["email"],
                    phone_number = account_dict["phone_number"],
                    password = account_dict["password"],
                    firstname = account_dict["firstname"],
                    lastname = account_dict["lastname"],
                    othername = account_dict["othername"],
                    join_date = account_dict["join_date"],
                    is_admin = account_dict["is_admin"]
                )
                self.accounts[account.account_id.hex] = account

        except Exception as e:
            raise e

    async def create_account(self, pool: Pool, account: Account) -> Optional[Account]:
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

    async def fetch_user(self, pool: Pool, accountid: UUID=None, email: EmailStr=None) -> Optional[Account]:
        """ Fetch user for self.accounts """
        try:
            if accountid:
                async with pool.acquire() as conn:
                    account_record = await conn.fetchrow("""
                        SELECT 
                            accts.*,
                            row_to_json(adm) AS admin,
                            COALESCE(
                                array_agg(
                                    json_build_object(
                                        'trip_id', trps.trip_id,
                                        'destination_id', trps.destination_id,
                                        'capacity', trps.capacity,
                                        'status', trps.status,
                                        'date', trps.date
                                    )
                                ) FILTER (WHERE trps.trip_id IS NOT NULL),
                                '{}'
                            ) AS trips
                        FROM
                            accounts accts
                        LEFT JOIN
                            admin adm
                        ON
                            accts.account_id = adm.admin_id
                        LEFT JOIN 
                            tickets tkt
                        ON 
                            accts.account_id = tkt.account_id
                        LEFT JOIN
                            trips trps
                        ON 
                            tkt.trip_id = trps.trip_id
                        LEFT JOIN 
                            destinations dests
                        ON
                            trps.destination_id = dests.destination_id
                        WHERE 
                            accts.account_id = $1
                        GROUP BY
                            accts.account_id, adm.admin_id
                    """, accountid)

                if not account_record:
                    return None

            elif email:
                async with pool.acquire() as conn:
                    account_record = await conn.fetchrow("""
                        SELECT 
                            accts.*,
                            row_to_json(adm) AS admin,
                            COALESCE(
                                array_agg(
                                    json_build_object(
                                        'trip_id', trps.trip_id,
                                        'destination_id', trps.destination_id,
                                        'capacity', trps.capacity,
                                        'status', trps.status,
                                        'date', trps.date
                                    )
                                ) FILTER (WHERE trps.trip_id IS NOT NULL),
                                '{}'
                            ) AS trips
                        FROM
                            accounts accts
                        LEFT JOIN
                            admin adm
                        ON
                            adm.account_id = accts.account_id
                        LEFT JOIN 
                            tickets tkt
                        ON 
                            tkt.account_id = accts.account_id
                        LEFT JOIN
                            trips trps
                        ON 
                            trps.trip_id = tkt.trip_id
                        LEFT JOIN 
                            destinations dests
                        ON
                            trps.destination_id = dests.destination_id
                        WHERE 
                            accts.email = $1
                        GROUP BY
                            accts.account_id, adm.admin_id
                    """, email)

                
                if not account_record:
                    return None

                # accout_dict.pop("password")

                # account = Account(
                #     account_id = account_dict["account_id"],
                #     email = account_dict["email"],
                #     phone_number = account_dict["phone_number"],
                #     passwordb= account_dict["password"],
                #     firstname = account_dict["firstname"],
                #     lastname = account_dict["lastname"],
                #     othername = account_dict["othername"],
                #     join_date = account_dict["join_date"],
                #     is_admin = account_dict["is_admin"],
                #     admin = Admin(
                #         admin_id = account_dict["admin_id"],
                #         account_id = account_dict["account_id"],
                #         roles = account_dict["roles"],
                #         date = account_dict["date"]
                #     )
                # )
        
            
            # pprint.pp(account_record)
            account_dict = dict(account_record)
            # pprint.pp(account_dict)

            if account_dict['admin']:
                account_dict['admin'] = json.loads(account_dict['admin'])
        
            return account_dict
        except Exception as e:
            raise e
    
    async def fetch(self, pool):
        """ Fetch all account data """
        try:
            async with pool.acquire() as conn:
                records = await conn.fetch("""
                    SELECT 
                        acct.*,
                        COALESCE(array_agg(trps.*) FILTER (WHERE trps.* IS NOT NULL), '{}') AS trips
                    FROM
                        accounts acct
                    LEFT JOIN
                        admin adm
                    ON 
                        adm.account_id = acct.account_id
                    LEFT JOIN
                        tickets tkt
                    ON 
                        tkt.account_id = acct.account_id
                    LEFT JOIN
                        trips trps
                    ON 
                        trps.trip_id = tkt.trip_id
                    GROUP BY
                        acct.account_id
                """)

            if not records:
                return None

            # pprint.pp(records)

            accounts = [dict(record) for record in records]
            return accounts

        except Exception as e:
            raise e
