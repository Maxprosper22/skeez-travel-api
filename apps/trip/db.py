from asyncpg import Pool

async def create_table(pool: Pool) -> None:
    """ Create a table for storing trips in database """

    async with pool.acquire() as conn:
        await conn.execute("CREATE TABLE IF NOT EXISTS trips (trip_id UUID PRIMARY KEY, destination TEXT NOT NULL, capacity INTEGER NOT NULL, slots UUID[], status TEXT NOT NULL, date TIMESTAMP NOT NULL)")
