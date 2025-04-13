from asyncpg import create_pool, Pool
from dynaconf import Dynaconf

async def db_conn(config: Dynaconf) -> str:
    """ Initialize database connection """

    DB_USER = config.database.user
    DB_PASS = config.db_password
    DB_HOST = config.database.host
    DB_PORT = config.database.port
    DB_NAME = config.database.name

    dsn = f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return dsn


async def db_pool(dsn: str, loop) -> Pool:
    """ DB connection pool """

    pool = await create_pool(dsn=dsn, loop=loop)
    return pool
