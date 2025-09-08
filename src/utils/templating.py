from sanic import Sanic
from jinja2 import Environment, PackageLoader, PrefixLoader, select_autoescape

async def setupTemplating(app: Sanic) -> None:
    """ Create and load templating environment """

    loaders = {
        'main': PackageLoader("src", "templates"),
        'admin': PackageLoader("src.blueprints.admin", "templates"),
    }

    env = Environment(
        loader=PrefixLoader(loaders),
        autoescape=select_autoescape()
    )

    return env

    

