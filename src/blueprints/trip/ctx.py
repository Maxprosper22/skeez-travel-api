from sanic import Sanic

from .models.trip import Trip, TripStatus
from .api import createTrip, cancelTrip, endTrip, startTrip, stopTrip, fetchTrip, fetchTrips

async def register_trip_ctx(app: Sanic) -> None:
    """ Function to add TripManager to app context """

    app.ctx.tripCtx = {
        'create_trip': createTrip,
        'cancel_trip': cancelTrip,
        'end_trip': endTrip,
        'start_trip': startTrip,
        'stop_trip': stopTrip,
        'fetch_trip': fetchTrip,
        'fetch_trips': fetchTrips,
        'tripStatus': TripStatus,
        'trip': Trip
    }
