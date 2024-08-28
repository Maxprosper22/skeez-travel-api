from sanic import Sanic, Request

async def authorize(request: Request):
    """ Authorization Middleware. Checks requests for access rights """
    pass

async def authenticate(request: Request):
    """ Authentication endpoint. REsponds to sign in requests """

    try:
        pass
    except Exception as e:
        raise e

async def signin(request: Request):
    """ Sign in endpoint """

    pass

async def signup(request: Request):
    """ Sign up end point. Handles user registration. """
    try:
        pass
    except Exception as e:
        raise e

async def signout(request: Request):
    """ Sign out endpoint """
    try:
        pass
    except Exception as e:
        raise e
