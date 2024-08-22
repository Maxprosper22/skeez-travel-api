from sanic import Sanic

from orb.views import index, home

async def load_url(app: Sanic):
    """ load application urls """

    app.add_route(index, '/', methods=['GET'])
    app.add_route(home, '/home', methods=['GET'])
