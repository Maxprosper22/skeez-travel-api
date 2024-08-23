import toml
from dotenv import load_dotenv
from sanic import Sanic

from orb.utils.env_to_toml import interpolate_env_vars
from orb.utils.setup_db import db_conn, db_pool, setupDB
# from orb.utils.setup_config import setupConfig
from orb.utils.setup_templating import setupTemplating
from orb.utils.setup_urls import setupUrls

# from orb.urls import load_url
# from orb.views import index, home

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

        # Setup database tables
        await setupDB(app)

        # app.ctx.pwd_security = PasswordSecurity()

        # Define template object
        await setupTemplating(app)

        # Setup ECDSA keys
        # await setupECDSA_Keys(app)

        # Setup application routing
        await setupUrls(app)
        # await load_url(app)

    # app.register_listener(applicationSetup, 'before_server_start')

    return app

# app.add_route(index, '/', methods=['GET'])
# app.add_route(home, '/home', methods=['GET'])

# if __name__ == "__main__":
    # app.run()
