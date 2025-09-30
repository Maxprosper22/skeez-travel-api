from dotenv import load_dotenv
from sanic import Sanic
from sanic.response import html as sanhtml, json as sanjson, file as sanfile
from sanic.log import logger
from sanic_ext import Extend
# from sanic_cors import CORS, cross_origin
import toml
import os
from pathlib import Path
from asyncio import create_subprocess_shell
from asyncio.subprocess import PIPE

import httpx, aiohttp

from src.utils.db import db_conn, db_pool
# from src.utils.templating import setupTemplating

from src.services import register_services
from src.blueprints import register_apps

# from src.services.mail import load_mail_config

from src.middlewares import setup_middleware
from src.urls import router

import pprint
# pprint.pp(os.__dir__())

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
        
async def load_paystack_config(config):
    """ Load paystack configuration """
    env = config.get('app')["ENV"]
    match env:
        case 'dev':
            paystack_config = config.get('dev', {})['paystack']
            paystack_config['SECRET_KEY'] = os.getenv("TEST_PAYSTACK_SECRET_KEY")
            paystack_config['PUBLIC_KEY'] = os.getenv("TEST_PAYSTACK_PUBLIC_KEY")

            if not paystack_config['SECRET_KEY']:
                raise ValueError("Paystack Secret key missing")
            elif not paystack_config['PUBLIC_KEY']:
                raise ValueError('Paystack public key missing')

            return paystack_config

        case 'prod':
            paystack_config = config.get('prod', {})['paystack']
            paystack_config['SECRET_KEY'] = os.getenv("PAYSTACK_SECRET_KEY")
            paystack_config['PUBLIC_KEY'] = os.getenv("PAYSTACK_PUBLIC_KEY")
            if not paystack_config['SECRET_KEY']:
                raise ValueError("Paystack Secret key missing")
            elif not paystack_config['PUBLIC_KEY']:
                raise ValueError('Paystack public key missing')

            return paystack_config


def create_app() -> Sanic:
    """" Application factory """

    app = Sanic("Skrid")

    # Configuration
    app.config.FRONTEND_DIR = Path(__file__).parent.parent / "skrid-web"
    app.config.DIST_DIR = app.config.FRONTEND_DIR / "dist"

    # Serve static assets (JS, CSS, etc.) from dist/assets
    app.static("/assets", app.config.DIST_DIR / "assets", name="assets")

    app.config.CORS_ORIGINS = ["http://127.0.0.1:8080", "http://localhost:3000", "http://127.0.0.1:3000"]
    app.config.CORS_SUPPORTS_CREDENTIALS = True
    app.config.CORS_AUTOMATIC_OPTIONS = True
    app.config.CORS_ALLOW_HEADERS = ['Origin', 'Accept', 'Content-Type', 'Access-Control-Allow-Origin', 'Authorization']
    Extend(app)


    # Serve index.html for all non-static routes to support TanStack Router
    @app.get("/<path:path>")
    async def serve_index(request, path: str):
        pprint.pp(app.config.FRONTEND_DIR)
        index_path = app.config.DIST_DIR / "index.html"
        # pprint.pp(index_path)
        if not index_path.exists():
            logger.error("index.html not found. Ensure `npm run build` has been run.")
            return sanhtml("Frontend not built. Run `npm run build` in skrid-web.", status=500)
        return await sanfile(index_path)


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
        # app.ctx.mailConfig = await load_mail_config(config)

        # Set up paystack configuration
        app.ctx.PaystackConfig = await load_paystack_config(config)

        # Set up aiohttp ClientSession
        app.ctx.aiohttpClient = aiohttp.ClientSession()
        # httpxClient
        app.ctx.httpxClient = httpx.AsyncClient()
        # Set up templating
        # app.ctx.template_env = await setupTemplating(app)

        # Setup ECDSA keys
        await register_services(app)

        await setup_middleware(app)
        # Setup application routing
        await router(app)
        # Register applications
        await register_apps(app)


    return app

# if __name__ == "__main__":
    # app.run()
