from sanic import Sanic

from orb.views import index, post

async def setup_urls(app: Sanic): 
    """ Set up application routing 
    
    Arguments:
        App: Sanic application instance

    Returns:
        None
    """

    app.add_route(index, '/', methods=['GET'])
    app.add_route(post, '/post/<postid>', methods=['GET'])
