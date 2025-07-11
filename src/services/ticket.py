from asyncpg import Pool
from uuid import UUID

class TicketService:

    @classmethod
    async def create_table(cls, pool: Pool):
        """ Creayes table if doesn't exists """

        async with pool.acquire() as conn:
            await conn.execute("""CREATE TABLE IF NOT EXISTS tickets (
                trip_id UUID REFERENCES trips,
                account_id UUID REFERENCES accounts,
                PRIMARY KEY(trip_id, account_id)
            )""")
