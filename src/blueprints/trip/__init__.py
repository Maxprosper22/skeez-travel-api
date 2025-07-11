from sanic import Sanic, Blueprint

from .urls import router

async def setup_trip_app(app: Sanic):
    """ Set up trip application """
    
    await router(app)  # Set up routing
    # await register_trip_ctx(app)

    # Instantiate trip manager
    # app.ctx.TripManager.

