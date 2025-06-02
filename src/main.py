from dotenv import load_dotenv
from sanic import Sanic
import toml, os

from src.utils.db import db_conn, db_pool
from config import settings
from src.utils.templating import setupTemplating
# from orb.utils.keys import setupECDSA_Keys
from src.utils.registry import register_apps

from src.routes import setup_urls

load_dotenv()

def load_config(file_path):
    try:
        with open(file_path, "r") as config_file:
            return toml.load(config_file)
    except FileNotFoundError:
        raise Exception(f"Configuration file {file_path} not found")
    except toml.TomlDecodeError:
        raise Exception(f"Invalid TOML format in {file_path}")

def create_app() -> Sanic:
    """" Application factory """

    # try:

    app = Sanic("Skrid")
    app.static("/static", "./src/assets")

    # app.config.templating_enable_async = True
    # app.config.templating_path_to_templates = 'orb/templates/'
    
    @app.listener("before_server_start")
    async def applicationSetup(app, loop):
        """ Server setup """
        
        # Apply the configuration to the Sanic app
        config = load_config("config.toml")
        app.config.update(config.get("app", {}))  # Update with 'app' section
        
        # Load database config and add the password from environment
        db_config = config.get("database", {})
        db_config["DB_PASSWORD"] = os.getenv("DB_PASSWORD")  # Get password from env
        if not db_config["DB_PASSWORD"]:
            raise ValueError("DB_PASSWORD environment variable is not set")
        app.config.update(db_config)

        # Setup database connection
        dsn = await db_conn(config=app.config)
        app.ctx.pool = await db_pool(dsn, loop)

        # app.ctx.pwd_security = PasswordSecurity()

        # Define template object
        app.ctx.template_env = await setupTemplating(app)

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
