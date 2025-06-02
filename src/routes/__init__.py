from sanic import Sanic

from src.views import index, notifications_handler, account_handler, destinations_handler, booking_handler, signin, signup, dashboard

async def setup_urls(app: Sanic): 
    """ Set up application routing 
    
    Arguments:
        App: Sanic application instance

    Returns:
        None
    """

    app.add_route(index, '/', methods=['GET'])
    app.add_route(dashboard, '/dashboard', methods=['GET', 'POST'])
    app.add_route(destinations_handler, '/destinations', methods=['GET'])
    # app.add_route(booking_handler, '/book', methods=["GET", "POST"])
    app.add_route(notifications_handler, '/notifications', methods=['GET', 'POST'])
    app.add_route(account_handler, '/account', methods=['GET', 'POST'])
    app.add_route(signin, '/account/auth/signin', methods=['GET', 'POST'])
    app.add_route(signup, '/account/auth/signup', methods=['GET', 'POST'])
    # app.add_route(admin, '/admin', methods=['GET', 'POST'])
