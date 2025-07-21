from sanic import Sanic, Blueprint
from sanic.request import Request
from sanic.response import redirect
from .views import dashboard, signin, TripView, view_trips, create_trip, start_trip, end_trip, cancel_trip, new_admin

async def index(request: Request) -> None:
    redirect('/admin/dashboard')

async def router(bp: Blueprint) -> None:
    """ Set up routing for admin blueprint """
    
    bp.add_route(index, '/')
    # bp.add_route(dashboard, '/dashboard', methods=['GET'])
    bp.add_route(new_admin, '/new-admin', methods=['POST'])
    bp.add_route(signin, '/auth/signin', methods=['POST'])
    bp.add_route(view_trips, '/board/trips', methods=['GET'])
    bp.add_route(TripView.as_view(), '/trip/:trip_id')
    bp.add_route(create_trip, '/trip/create', methods=['GET', 'POST'])
    bp.add_route(start_trip, '/trip/:trip_id/start/', methods=['GET', 'POST'])
    bp.add_route(end_trip, '/trip/:trip_id/end/', methods=['GET', 'POST'])
    bp.add_route(cancel_trip, '/trip/:trip_id.cancel_trip', methods=['GET', 'POST'])

