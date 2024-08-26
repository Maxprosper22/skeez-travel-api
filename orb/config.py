from sanic import Sanic

from dotenv import load_dotenv

load_dotenv()

async def setupConfig(app: Sanic) -> None:
    """ Setup application configuration """
    
    # config = os.gen
    # app.update_config


