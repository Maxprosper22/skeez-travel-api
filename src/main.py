from dotenv import load_dotenv
from sanic import Sanic
import toml
import os

from src.utils.db import db_conn, db_pool
from src.utils.templating import setupTemplating

from src.services import register_services
from src.blueprints import register_apps

from src.services.mail import load_mail_config

# from src.routes import setup_urls

import pprint

load_dotenv()

def load_config(file_path):
    try:
        with open(file_path, "r") as config_file:
            return toml.load(config_file)
    except FileNotFoundError:
        raise Exception(f"Configuration file {file_path} not found")
    except toml.TomlDecodeError:
        raise Exception(f"Invalid TOML format in {file_path}")

async def load_database_config(config):
    """ Load database config. Dependent on tye environment """
    env = config.get('app')["ENV"]
    match env:
        case "dev":
            # Load database config and add the password from environment
            db_config = config.get("dev", {})['database']
            db_config["DB_PASSWORD"] = os.getenv("DEV_DB_PASSWORD")  # Get password from env
            if not db_config["DB_PASSWORD"]:
                raise ValueError("DB_PASSWORD environment variable is not set")

            return db_config
        case "prod":
            # Load database config and add the password from environment
            db_config = config.get("prod", {})['database']
            db_config["DB_PASSWORD"] = os.getenv("DB_PASSWORD")  # Get password from env
            if not db_config["DB_PASSWORD"]:
                raise ValueError("DB_PASSWORD environment variable is not set")

            return db_config
        

def create_app() -> Sanic:
    """" Application factory """

    app = Sanic("Skrid")
    app.static("/static", "./src/assets")
    
    @app.listener("before_server_start")
    async def application_setup(app, loop):
        """ Server setup """
        
        # Apply the configuration to the Sanic app
        config = load_config("config.toml")
        # pprint.pp(config)

        # Update with 'app' section
        app.config.update(config)
        # pprint.pp(app.config)

        db_config = await load_database_config(config)

        # Setup database connection
        dsn = await db_conn(config=db_config)
        app.ctx.pool = await db_pool(dsn, loop)

        # Load email config
        app.ctx.mailConfig = await load_mail_config(config)

        # Set up templating
        app.ctx.template_env = await setupTemplating(app)

        # Setup ECDSA keys
        await register_services(app)

        # Setup application routing
        # await setup_urls(app)

        # Register applications
        await register_apps(app)


    return app

# if __name__ == "__main__":
    # app.run()
