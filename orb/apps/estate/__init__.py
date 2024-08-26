import toml

from sanic import Sanic, Blueprint

from .urls import setupUrls

async def main(app: Sanic) -> Blueprint:
    """ Estate application """

    estateApp = Blueprint('estate', url_prefix='estate')

    estateApp.static('/static.estate', 'orb/apps/estate/assets/')

    # Setup application routing
    await setupUrls(app, estateApp)

    return estateApp

