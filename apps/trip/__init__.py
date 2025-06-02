from sanic import Sanic, Blueprint

from .models.trip import Trip, SlotList
from .urls import router
from .ctx import register_trip_ctx
from .template_loader import trip_loader
from .db import create_table

async def setup_trip_app(app: Sanic):
    """ Set up trip application """
    
    await router(app)  # Set up routing
    await register_trip_ctx(app)

    # Create trips table
    await create_table(app.ctx.pool)
