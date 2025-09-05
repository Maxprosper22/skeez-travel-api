import jwt
from sanic.request import Request
from sanic.response import json as sanjson, html as sanhtml

async def check_auth(request: Request):
    """ Checks if user is authenticated """

    app = request.app
    pool = app.ctx.pool

    cookie_token
