from sanic import Sanic

from .account import setup_accounts
from .trip import setup_trip_app
from .admin import setup_admin_app

async def register_apps(app: Sanic) -> None:
    """
        Services registry
        Convention: Import setup function (prefix with `setup`) of each app
    """

    admin_bp = await setup_admin_app(app)
    app.blueprint(admin_bp)
    
    account_bp = await setup_accounts(app)
    app.blueprint(account_bp)

    # trip_bp = await setup_trip_app(app)
    # app.blueprint(trip_bp)
