# import traceback

from asyncpg import create_pool
from sanic import Sanic

# from orb.apps.auth import create_auth_table
# from orb.apps.product import create_product_table
# from orb.apps.user import create_user_table

async def db_conn(config: dict) -> str:
	""" Initialize database connection """

	DB_USER = config['user']
	DB_PASS = config['password']
	DB_HOST = config['host']
	DB_PORT = config['port']
	DB_NAME = config['name']

	dsn = f'postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

	return dsn

async def db_pool(dsn: str, loop):
	""" DB connection pool """
	
	pool = await create_pool(dsn=dsn, loop=loop)
	return pool

async def setupDB(app: Sanic) -> None:
    """ Create database tables """
    try:
		# await create_auth_table(app)
		# await create_user_table(app)
		# await create_product_table(app)
        pass

    except Exception as e:
        # print(traceback.format_exc(e))
        raise e
