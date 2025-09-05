from asyncpg import Pool
from uuid import UUID

class TicketService:

    async def create_table(self, pool: Pool):
        """ Creayes table if doesn't exists """

        async with pool.acquire() as conn:
            await conn.execute("""CREATE TABLE IF NOT EXISTS tickets (
                trip_id UUID REFERENCES trips,
                account_id UUID REFERENCES accounts,
                PRIMARY KEY(trip_id, account_id)
            )""")

    async def fetch_ticket(self, pool):
        """ Fetch ticket data """

        async with pool.acquire() as conn:
            trip_records = await conn.fetch("""SELECT trips.* FROM courses c
       JOIN student_courses sc ON c.course_id = sc.course_id
       WHERE sc.student_id = $1""")
