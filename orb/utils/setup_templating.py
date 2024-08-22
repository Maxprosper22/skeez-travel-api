from sanic import Sanic
from jinja2 import Environment, PackageLoader, FileSystemLoader

async def setupTemplating(app: Sanic) -> None:
    """ Create and load templating environment """
    
    package_loader = PackageLoader('orb', 'templates')

    env = Environment(loader=package_loader)

    app.ctx.TemplateEnv = env

    

