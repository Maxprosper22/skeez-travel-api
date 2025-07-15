from sanic import Sanic, Blueprint
from .urls import router

async def setup_accounts(app: Sanic):
    """ Set up account management """

    account_bp = Blueprint("account", url_prefix="/account")
    account_bp.static('/static', 'src/blueprints/account/assets')
    
    await router(account_bp)

    return account_bp
