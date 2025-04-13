from sanic import Sanic

# from orb.services.estate import main as estate_factory

async def register_apps(app: Sanic) -> None:
    """ Application registry """
    
    # estate = await estate_factory(app)

    # app.blueprint(estate)
