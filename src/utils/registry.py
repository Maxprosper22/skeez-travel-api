from sanic import Sanic

from apps.trip import setup_trip_app
from apps.admin import setup_admin_app

async def register_apps(app: Sanic) -> None:
    """
        Services registry
        Convention: Import setup function (prefix with `setup`) of each app
    """

    admin_app = await setup_admin_app(app)
    app.blueprint(admin_app)
    
    await setup_trip_app(app)
