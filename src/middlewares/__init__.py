from sanic import Sanic
from .session import session

async def setup_middleware(app: Sanic) -> None:
    """ Setup application middleware """

    app.register_middleware(session, 'request')
