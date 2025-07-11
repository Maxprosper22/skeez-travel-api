from sanic import Sanic
from asyncpg import Pool

async def create_table(pool: Pool):
    """ Create admin table in database """

    async with pool.acquire() as conn:
        await conn.execute("CREATE TABLE IF NOT EXISTS admin  (admin_id UUID PRIMARY KEY, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")
