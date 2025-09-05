from sanic import Sanic, Blueprint
from sanic.request import Request
from sanic.response import redirect
from .views import dashboard, signin, TripView, view_accounts, fetch_accounts, view_trips, fetch_trips, create_trip, start_trip, end_trip, cancel_trip, new_admin, view_destinations, new_destination

async def index(request: Request) -> None:
    return redirect('/admin/dashboard')

async def router(bp: Blueprint) -> None:
    """ Set up routing for admin blueprint """
    
    bp.add_route(index, '/')
    bp.add_route(dashboard, '/dashboard', methods=['GET'])
    bp.add_route(view_accounts, '/accounts', methods=['GET'])
    bp.add_route(fetch_accounts, '/api/accounts', methods=['GET'])
    bp.add_route(view_destinations, '/destinations', methods=['GET'])
    bp.add_route(new_destination, '/destinations/new', methods=['POST'])
    bp.add_route(new_admin, '/create', methods=['POST'])
    bp.add_route(signin, '/auth/signin', methods=['POST']),
    bp.add_route(view_trips, '/trips', methods=['GET'])
    bp.add_route(fetch_trips, '/api/trips', methods=['GET'])
    bp.add_route(TripView.as_view(), '/trip/<tripid>')
    bp.add_route(create_trip, '/trip/create', methods=['GET', 'POST'])
    bp.add_route(start_trip, '/trip/<trip_id>/start/', methods=['GET', 'POST'])
    bp.add_route(end_trip, '/trip/<trip_id>/end/', methods=['GET', 'POST'])
    bp.add_route(cancel_trip, '/trip/<trip_id>/cancel', methods=[ 'POST'])

