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

from src.services import register_services
from src.services.celery_app import app as celeryapp, email_verification, email_reset_link
from src.services.mail import load_mail_config

from src.services.magiclink import SecureMagicLink


from src.blueprints import register_apps

from cryptography.fernet import Fernet

# from src.services.mail import load_mail_config

from src.middlewares import setup_middleware
from src.urls import router

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


def load_database_config():
    """ Load database config. Dependent on the environment """
    try:
        db_config = {}
        db_config["DB_NAME"] = os.getenv("DB_NAME")
        db_config["DB_USER"] = os.getenv("DB_USER")
        db_config["DB_HOST"] = os.getenv("DB_HOST")
        db_config["DB_PROT"] = os.getenv("DB_PORT")
        db_config["DB_PASSWORD"] = os.getenv("DB_PASSWORD")  # Get password from env

        if not db_config["DB_PASSWORD"]:
            raise ValueError("DB_PASSWORD environment variable is not set")

        return db_config
    except Exception as e:
        raise e


def load_paystack_config(config):
    """ Load paystack configuration """
    try:
        config['paystack'] = {}
        config['paystack']['SECRET_KEY'] = os.getenv("PAYSTACK_SECRET_KEY")
        config['paystack']['PUBLIC_KEY'] = os.getenv("PAYSTACK_PUBLIC_KEY")

        if not config['paystack']['SECRET_KEY']:
            raise ValueError("Paystack Secret key missing")
        elif not config['paystack']['PUBLIC_KEY']:
            raise ValueError('Paystack public key missing')

        # return paystack_config

    except Exception as e:
        raise e


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
        # pprint.pp(app.config.FRONTEND_DIR)
        index_path = app.config.DIST_DIR / "index.html"
        # pprint.pp(index_path)
        if not index_path.exists():
            logger.error("index.html not found. Ensure `npm run build` has been run.")
            return sanhtml("Frontend not built. Run `npm run build` in skrid-web.", status=500)
        return await sanfile(index_path)


    app.static("/static", "./src/assets")

    # @app.main_process_start
    # async def application_setup(app, loop):
        # """ Server setup """
        
        # Load encryption key
    app.ctx.ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY').encode()
        
    fernetkey = Fernet(app.ctx.ENCRYPTION_KEY) 
    app.ctx.fernet = fernetkey

    # Set up magic links
    app.ctx.EmailVerificationLink = SecureMagicLink(
        app=app,
        secret_key=app.ctx.ENCRYPTION_KEY,
        link_type="verify"
    )
    app.ctx.PasswordResetLink = SecureMagicLink(
        app=app,
        secret_key=app.ctx.ENCRYPTION_KEY,
        link_type="reset"
    )

    # Create celery app ctx
    app.ctx.CeleryApp = celeryapp
    app.ctx.tasks ={
        'email_verification': email_verification,
        'email_reset_link': email_reset_link
    }


    # Apply the configuration to the Sanic app
    config = load_config("config.toml")
    # pprint.pp(config)

    # Update with 'app' section
    # app.config.update(config)

    db_config = load_database_config()
    # app.config.update(db_config)


    # Load email config
    app.ctx.mailConfig = load_mail_config()

        # Set up paystack configuration
    paystackConfig = load_paystack_config(config)


    app.config.update(config)



    @app.before_server_start
    async def setup(app, loop):
        """ Set up application workers """
        # pprint.pp(app.config)

        # Setup database connection
        dsn = await db_conn(db_config)
        app.ctx.pool = await db_pool(dsn, loop)

        # Set up aiohttp ClientSession
        app.ctx.aiohttpClient = aiohttp.ClientSession()
        # httpxClient
        app.ctx.httpxClient = httpx.AsyncClient()

        # Set up templating
        # app.ctx.template_env = await setupTemplating(app)

        # Setup application routing
        await router(app)
        # Register applications
        await register_apps(app)

        await register_services(app)
        await setup_middleware(app)

    return app

# if __name__ == "__main__":
    # app.run()
