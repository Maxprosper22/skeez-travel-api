from sanic import Sanic

# from src.blueprints.account import setup_accounts
# from src.blueprints.trip import setup_trip_app
# from src.blueprints.admin import setup_admin_app

async def regster_apps(app: Sanic) -> None:
    """
        Services registry
        Convention: Import setup function (prefix with `setup`) of each app
    """

    # admin_app = await setup_admin_app(app)
    # app.blueprint(admin_app)
    #
    # await setup_accounts(app)
    # await setup_trip_app(app)
