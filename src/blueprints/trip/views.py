from sanic import Sanic, Blueprint
from sanic.request import Request
from sanic.response import html as sanhtml, json as sanjson, text as santext

# from .api import createTrip, cancelTrip, startTrip, endTrip, fetchTrip, fetchTrips, stopTrip

async def fetch_trips(request: Request):
    """ 
        Retrieve data on available trips
        Method: Get
    """

    app = request.app
    pool = app.ctx.pool
    trip_manager = app.ctx.TripManager

    trips = await fetchTrips(app, pool)
    
    if trips == None:
        return sanjson({})
    
    for trip in trips:
        trips[trip.trip_id.hex()] = trip.model_dump

    return sanjson(trips)

async def fetch_trip(request: Request, trip_id: str) :
    """ 
        Retrieve data for a specific trip
        Method: Get
    """
    
    app = request.app
    pool = app.ctx.pool
    trip_manager = app.ctx.TripTanager

    trip = trip_manager.fetch_by_id(trip_id)

    if trip_id == None:
        return (401, "Invalid operation. No trip id provided")  # A tuple containing a status code and a message: (status, message)

async def book(request: Request, trip_id: str):
    """ 
        Register a passenger for a trip
        Method: Post
    """

async def unbook(request: Request, trip_id: str, passenger_id: str):
    """
        Remove a passenger from the list of passengers
        Method: Patch
    """
