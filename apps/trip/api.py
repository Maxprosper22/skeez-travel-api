import asyncio
from pydantic import BaseModel, Field, field_validator, model_validator
from sanic import Sanic
from asyncpg.pool import Pool
from uuid import UUID
from typing import Optional
from returns.maybe import Maybe, maybe, Some, Nothing

from .models.trip import TripStatus, Trip


async def createTrip(pool: Pool, trip: Trip) -> Optional[Trip]:
    """ Create a trip instance """
    print(trip.status.name)
    async with pool.acquire() as conn:
        await conn.execute("INSERT INTO trips (trip_id, destination, capacity, slots, status, date) VALUES ($1, $2, $3, $4, $5, $6)", trip.trip_id, trip.destination, trip.capacity, trip.slots, trip.status.value, trip.date)
        
        await asyncio.sleep(1000)
        trip_record = await conn.fetchrow("SELECT * FROM trips WHERE trip_id=$1", trip.trip_id)

    if not trip_record:
        return None

    trip_dict = dict(trip_record) # Convert Record object to dictionary
    trip_dict['status'] = TripStatus(trip_dict['status'])
    new_trip = Trip(**trip_dict)  # Cast dictionary to Trip object
        
    return new_trip



async def cancelTrip(trip_id: UUID) -> Optional[Trip]:
    """ Cancels trip """

    trip = await fetch_trip(trip_id)

    match trip:
        case Trip(trip_id):
            trip.status = TripStatus.CANCELLED
            return Trip
        case None:
            return None
        case _:
            return "Unknown error"

async def endTrip(app: Sanic, trip_id: UUID):
    """ Update trip id """

async def fetchTrip(pool: Pool, trip_id: UUID) -> Optional[Trip]:
    """ Retrieve trip with matching id """

    async with pool.acquire() as conn:
        trip_rec = await conn.fetchrow("SELECT * FROM trips WHERE trip_id=$1", trip_id)
    
    if trip_rec:
        trip = dict(trip_rec)
        trip['status'] = TripStatus(trip['status'])
        return Trip(**trip)
    
    return None

async def fetchTrips(pool: Pool) -> Optional[list[Trip]]:
    """ Fetch trips """

    async with pool.acquire() as conn:
        trip_records = await conn.fetch("SELECT * FROM trips")
    
    if trip_records:
        trips = []
        for trip in trip_records:
            trip = dict(trip)
            trip['status'] = TripStatus(trip['status'])
            trips.append(trip)

        return trips

    return None

async def startTrip(pool: Pool, trip_id: str,):
    """ Start a trip """

async def stopTrip(pool: Pool, trip_id: str):
    """ Stop monitoring process """
