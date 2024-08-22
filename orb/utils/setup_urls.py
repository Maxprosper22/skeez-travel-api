from sanic import Sanic

from orb.urls import load_url

async def setupUrls(app: Sanic):
    """ Set up application routing 
    
    Arguments:
        App: Sanic application instance

    Returns:
        None
    """

    await load_url(app)
