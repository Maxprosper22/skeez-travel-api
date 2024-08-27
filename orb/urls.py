from sanic import Sanic

from orb.views import index, home, timeline, post

async def setup_urls(app: Sanic): 
    """ Set up application routing 
    
    Arguments:
        App: Sanic application instance

    Returns:
        None
    """

    app.add_route(index, '/', methods=['GET'])
    app.add_route(home, '/home', methods=['GET'])
    app.add_route(timeline, '/timeline', methods=['GET'])
    app.add_route(post, '/post/<postid>', methods=['GET'])
