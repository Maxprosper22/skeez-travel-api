from sanic import Sanic, Blueprint

from orb.services.estate.views import index, about

async def setupUrls(app: Sanic, blueprint: Blueprint) -> None:
    """ Register map URLs to handlers """

    blueprint.add_route(index, '/', methods=['GET'])
    blueprint.add_route(about, '/about', methods=['GET'])
