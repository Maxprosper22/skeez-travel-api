from asyncpg import create_pool, Pool
from dynaconf import Dynaconf
# from sanic.

async def db_conn(config: Dynaconf) -> str:
    """ Initialize database connection """

    print(f"DB config: {type(config)}")

    DB_USER = config["DB_USER"]
    DB_PASS = config["DB_PASSWORD"]
    DB_HOST = config["DB_HOST"]
    DB_PORT = config["DB_PORT"]
    DB_NAME = config["DB_NAME"]
    # DB_PASSWORD = config["DB_PASSWORD"]
    
    dsn = f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return dsn


async def db_pool(dsn: str, loop) -> Pool:
    """ DB connection pool """

    pool = await create_pool(dsn=dsn, loop=loop, statement_cache_size=0)
    return pool
