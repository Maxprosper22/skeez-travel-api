from asyncpg import create_pool

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


