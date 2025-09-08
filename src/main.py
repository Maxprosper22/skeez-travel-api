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
from src.utils.templating import setupTemplating

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

    # Optional API route for testing
    @app.get("/api/hello")
    async def hello_world(request):
        return sanjson({"message": "Hello from Sanic!"})

    # File reload signal handler
    @app.signal("watchdog.file.reload")
    async def file_reloaded():
        logger.info("Detected file changes, checking for rebuild...")
        do_rebuild = False
        reloaded_files = app.config.get("RELOADED_FILES", "").split(",")

        # Check if any changed files are JS/TS/TSX
        for filename in reloaded_files:
            if filename and filename.rsplit(".", 1)[-1] in ("js", "ts", "tsx"):
                do_rebuild = True
                break

        if do_rebuild:
            logger.info("Rebuilding frontend due to JS/TS/TSX changes...")
            try:
                rebuild = await create_subprocess_shell(
                    "npm run build",
                    stdout=PIPE,
                    stderr=PIPE,
                    cwd=app.config.FRONTEND_DIR,
                )
                stdout, stderr = await rebuild.communicate()

                if rebuild.returncode == 0:
                    logger.info("Frontend rebuild successful.")
                    for line in stdout.decode("ascii").splitlines():
                        logger.info(f"[rebuild] {line}")
                else:
                    logger.error("Frontend rebuild failed.")
                    for line in stderr.decode("ascii").splitlines():
                        logger.error(f"[rebuild error] {line}")
            except Exception as e:
                logger.error(f"Error during rebuild: {e}")
        else:
            logger.info("No rebuild needed (no JS/TS/TSX changes).")

    # Listener to initialize file watching (development only)
    @app.listener("before_server_start")
    async def setup_file_watcher(app, loop):
        if app.config.get("SANIC_ENV", "production") == "development":
            logger.info("Starting in development mode, setting up file watcher...")
            # Simulate file changes or integrate with watchdog (example below)
            # For watchdog integration, ensure `watchdog` is installed: `pip install watchdog`
            try:
                from watchdog.observers import Observer
                from watchdog.events import FileSystemEventHandler

                class FileChangeHandler(FileSystemEventHandler):
                    def on_any_event(self, event):
                        if event.is_directory:
                            return
                        if event.src_path.endswith((".js", ".ts", ".tsx")):
                            app.config["RELOADED_FILES"] = event.src_path
                            app.dispatch("watchdog.file.reload")

                observer = Observer()
                observer.schedule(FileChangeHandler(), app.config.FRONTEND_DIR, recursive=True)
                observer.start()
                logger.info("File watcher started for skrid-web directory.")
                app.ctx.observer = observer  # Store observer to stop it later
            except ImportError:
                logger.warning("Watchdog not installed. File watching disabled.")
        else:
            logger.info("Starting in production mode, no file watcher needed.")

    # Stop file watcher on server shutdown (development only)
    @app.listener("after_server_stop")
    async def stop_file_watcher(app, loop):
        if hasattr(app.ctx, "observer"):
            app.ctx.observer.stop()
            app.ctx.observer.join()
            logger.info("File watcher stopped.")

    app.static("/static", "./src/assets")

    # CORS(app)

    # pprint.pp(app.config.__dir__())
    app.config.CORS_ORIGINS = ["http://127.0.0.1:8080", "http://localhost:3000", "http://127.0.0.1:3000"]
    app.config.CORS_SUPPORTS_CREDENTIALS = True
    app.config.CORS_AUTOMATIC_OPTIONS = True
    app.config.CORS_ALLOW_HEADERS = ['Origin', 'Accept', 'Content-Type', 'Access-Control-Allow-Origin', 'Authorization']
    Extend(app)

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
        app.ctx.template_env = await setupTemplating(app)

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
