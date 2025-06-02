from sanic import Sanic, Blueprint

from .urls import router
from .template_loader import admin_loader
from .db import create_table
from .signals import create_trip_success, create_trip_failure, trip_status_update

async def setup_admin_app(app: Sanic) -> None:
    """ Set up admin application """

    await create_table(app.ctx.pool)

    admin_bp = Blueprint("admin", url_prefix="/admin")
    admin_bp.static('/static', './apps/admin/assets')
    
    # Add trip signals
    admin_bp.add_signal(create_trip_success, "trip.create.success")
    admin_bp.add_signal(create_trip_failure, "trip.create.failure")
    admin_bp.add_signal(trip_status_update, "trip.status.update")

    await router(admin_bp)  # Set up routing

    # print(admin_bp.__dir__())

    return admin_bp
