from sanic import Sanic, Blueprint

from .urls import router

async def setup_trip_app(app: Sanic) -> Blueprint:
    """ Set up trip application """
    
    # trip_bp = Blueprint("trips", url_prefix="/trips")
    await router(app)  # Set up routing
    
    # return trip_bp
