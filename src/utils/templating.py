from sanic import Sanic
from jinja2 import Environment, PackageLoader, PrefixLoader, select_autoescape

async def setupTemplating(app: Sanic) -> None:
    """ Create and load templating environment """

    loaders = {
        'main': PackageLoader("src", "templates"),
        'admin': PackageLoader("apps.admin", "templates"),
        'trip': PackageLoader("apps.trip", "templates")
    }

    env = Environment(
        loader=PrefixLoader(loaders),
        autoescape=select_autoescape()
    )

    return env

    

