from sanic import Sanic, Blueprint

from .views import index, add_media, fetch_media, delete_media

async def setupUrls(app: Sanic, blueprint: Blueprint) -> None:
    """ Setup media urls """

    blueprint.add_route(index, '/', methods=['GET'])
    blueprint.add_route(add_media, '/new', methods=['POST'])
    blueprint.add_route(fetch_media, '/media/<id>', methods=['GET'])
    blueprint.add_route(delete_media, '/media/<id>/delete', methods=['DELETE'])
