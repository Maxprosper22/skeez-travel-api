from sanic import Sanic, Blueprint

async def account_bp(app: Sanic) -> Blueprint:
    """ Setup account blueprint """

    bp = Blueprint('account', url_prefix='account')

    app.blueprint(bp)
        
