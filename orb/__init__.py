import toml
from dotenv import load_dotenv
from sanic import Sanic

from orb.utils.env_to_toml import interpolate_env_vars

from orb.db import db_conn, db_pool
# from orb.config import setupConfig
from orb.templating import setupTemplating
from orb.keys import setupECDSA_Keys
from orb.urls import setup_urls

from orb.registry import register_apps

load_dotenv()

def create_app() -> Sanic:
    """" Application factory """

    # try:

    app = Sanic("Orb")
    app.static("/static", "./orb/assets")

    # app.config.templating_enable_async = True
    # app.config.templating_path_to_templates = 'orb/templates/'
    
    @app.listener("before_server_start")
    async def applicationSetup(app, loop):
        """ Server setup """
            
        # Setup configuration
        config = toml.load("orb/config.toml")
        interpolate_env_vars(config)

        app.config.update_config(config)

        # Setup database connection
        dsn = await db_conn(config=config['database'])
        app.ctx.pool = await db_pool(dsn, loop)

        # app.ctx.pwd_security = PasswordSecurity()

        # Define template object
        await setupTemplating(app)

        # Setup ECDSA keys
        # await setupECDSA_Keys(app)

        # Setup application routing
        await setup_urls(app)

        # Register applications
        await register_apps(app)

    # app.register_listener(applicationSetup, 'before_server_start')

    return app

# app.add_route(index, '/', methods=['GET'])
# app.add_route(home, '/home', methods=['GET'])

# if __name__ == "__main__":
    # app.run()
