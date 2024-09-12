from sanic import Sanic

from orb.views import index, post, createpost, notifications_handler, chats_handler, profile_handler

async def setup_urls(app: Sanic): 
    """ Set up application routing 
    
    Arguments:
        App: Sanic application instance

    Returns:
        None
    """

    app.add_route(index, '/', methods=['GET'])
    app.add_route(post, '/post/<postid>', methods=['GET'])
    app.add_route(createpost, '/create-post', methods=['GET', 'POST'])
    app.add_route(notifications_handler, '/notifications', methods=['GET', 'POST'])
    app.add_route(chats_handler, '/chats', methods=['GET', 'POST'])
    app.add_route(profile_handler, '/profile', methods=['GET', 'POST'])
