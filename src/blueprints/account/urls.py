from sanic import Sanic, Blueprint
from sanic.request import Request
from sanic.response import redirect
from .views import account_info, signin, signup, account_trips

async def index(request: Request) -> None:
    redirect('/account/<accountid>')

async def router(bp: Blueprint) -> None:
    """ Set up routing for admin blueprint """
    
    bp.add_route(index, '/')
    bp.add_route(account_info, '/<accountid>', methods=['GET'])
    # bp.add_route(dashboard, '/dashboard', methods=['GET'])
    # bp.add_route(view_trips, '/<accountid>/trips', methods=['GET'])
    bp.add_route(signin, '/auth/signin', methods=['POST'])
    bp.add_route(signup, '/auth/signup', methods=['POST'])

