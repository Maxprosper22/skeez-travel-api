import asyncio
from pydantic import BaseModel, Field, field_validator, model_validator
from sanic import Sanic
from asyncpg.pool import Pool
from uuid import UUID
from typing import Optional
from datetime import datetime, timedelta
from returns.maybe import Maybe, maybe, Some, Nothing

from src.models.trip import TripStatus, Trip


class TripService:
    trips: Optional[list[Trip]] = []
    running: bool = False
    
    @classmethod
    async def run_trips(cls, app: Sanic, pool: Pool):
        """
            Run all trips in with pending and active statuses in self.trips. Runs on server startup.
        """
        try:
            for trip in self.trips:
                if trip.status == TripStatus.PENDING:
                    app.add_task(
                        cls.pending_trip_task,
                        name=f"trip-{trip.trip_id.hex}"
                    )
                elif trip.status == TripStatus.ACTIVE:
                    app.add_task(
                        cls.active_trip_task,
                        name=f"trip-{trip.trip_id.hex}"
                    )
        except Exception as e:
            raise e

    @classmethod
    async def pending_trip_task(cls, app: Sanic, trip: Trip) -> None:
        """ A method tracks the approaching date of a trip """
        try:
            count_down = trip.date - datetime.now()
            if datetime.now() >= trip.date:
                """
                    - Send alert to admin and users about the start of trip 
                    - Change trip status to active
                """
                cls.update_trip_status(
                    cls.pool,
                    trip=trip.trip_id,
                    status=TripStatus.ACTIVE
                )
                cls.app.cancel_task(name=f"trip-{trip.trip_id.hex}")

            if count_down.days != 0 and count_down.days <= 3:

                await asyncio.sleep(86400) # Sleep for 24 hours and check again
                # Send email and sms
                print(f"Hello there! Your trip to {trip.destination} is 5 days away. How's your packing going?")

        except Exception as e:
            raise e

    @classmethod
    async def active_trip_task(cls, trip: Trip) -> None:
        """ Tracks a trip which currently underway. """
        try:
            pass
        except Exception as e:
            raise e

    @classmethod
    async def create_trip(cls, pool: Pool, trip: Trip) -> Optional[dict]:
        """ Create a trip instance """
        print(trip.status.name)
        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO trips (
                    trip_id,
                    destination, 
                    capacity,
                    slots,
                    status,
                    date
                ) VALUES ($1, $2, $3, $4, $5, $6)
            """,
                trip.trip_id, trip.destination, trip.capacity, trip.slots, trip.status.value, trip.date
            )
        
            # await asyncio.sleep(1000)
            trip_record = await conn.fetchrow("SELECT * FROM trips WHERE trip_id=$1", trip.trip_id)
        # print(f"Trip created: {trip_record}")
        if not trip_record:
            return None
    
        trip_dict = dict(trip_record) # Convert Record object to dictionary

        trip_dict_copy = trip_dict.copy()  # Duplicate `trip_dict`
        trip_dict_copy['status'] = TripStatus(trip_dict_copy['status'])  # Convert trip status to TripStatus
        trip_cast = Trip(**trip_dict_copy)  # Cast dictionary to Trip object

        cls.trips.append(trip_cast)  # Cast trip dict to Trip object


        trip_dict['trip_id'] = trip_dict['trip_id'].hex
        trip_dict['date'] = trip_dict['date'].isoformat()
        
        return trip_dict


    @classmethod
    async def cancel_trip(cls, trip_id: UUID) -> Optional[Trip]:
        """ Cancels trip """

        trip = await fetch_trip(trip_id)
    
        match trip:
            case Trip():
                trip.status = TripStatus.CANCELLED

                return Trip
            case None:
                return None
            case _:
                return "Unknown error"

    @classmethod
    async def update_trip_status(cls, pool: Pool, trip_id: UUID, status: TripStatus):
        """
            Update trip (trip_id) status to (status). Status may be one of the following ['pending', 'active', 'cancelled', 'complete']
        """
        try:
            async with pool.acquire() as conn:
                modded_trip = await conn.execute("""
                    UPDATE trips SET status=$1 WHERE trip_id=$2
                """, status, trip_id)

            if modded_trip:
                updated_trip = dict(modded_trip)
                for trip in self.trips:
                    if trip.trip_id == trip_id:
                        trip.status = updated_trip["status"]

        except Exception as e:
            raise e        


    @classmethod
    async def db_fetch_trip(cls, pool: Pool, trip_id: UUID) -> Optional[Trip]:
        """ Retrieve trip with matching id """

        async with pool.acquire() as conn:
            trip_rec = await conn.fetchrow("SELECT * FROM trips WHERE trip_id=$1", trip_id)
    
        if trip_rec:
            trip = dict(trip_rec)
            trip['status'] = TripStatus(trip['status'])
            return Trip(**trip)
    
        return None

    @classmethod
    async def populate_trips(cls, pool: Pool) -> Optional[list[Trip]]:
        """
            Fetches all trips from database and populate `self.trips`. This method is to be run on server start up.

            Note: To access trips use `self.trips`
        """

        async with pool.acquire() as conn:
            trip_records = await conn.fetch("SELECT * FROM trips")
    
        if trip_records:
            for trip in trip_records:
                trip = dict(trip)
                trip['status'] = TripStatus(trip['status'])
                trip = Trip(**trip)
                cls.trips.append(trip)
                
            # return trips

        # return None

    
    @classmethod
    async def create_trip_table(cls, pool: Pool) -> None:
        """ Create a table for storing trips in database """

        try:
            async with pool.acquire() as conn:
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS trips (
                        trip_id UUID PRIMARY KEY,
                        destination TEXT NOT NULL,
                        capacity INTEGER NOT NULL,
                        slots UUID[],
                        status TEXT NOT NULL,
                        date TIMESTAMP NOT NULL
                    )
                """)
        except Exception as e:
            raise e

    @classmethod
    async def create_ticket_table(cls, pool: Pool):
        """ Create ticket table """
        try:
            async with pool.acquire() as conn:
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS tickets (
                        ticket_id UUID PRIMARY KEY,
                        account_id UUID REFERENCES accounts(account_id),
                        trip_id UUID REFERENCES trips(trip_id)
                    )
                """)

        except Exception as e:
            raise e

    @classmethod
    async def startTrip(cls, pool: Pool, trip_id: str,):
        """ Start a trip """

    @classmethod
    async def stopTrip(cls, pool: Pool, trip_id: str):
        """ Stop monitoring process """

    @classmethod
    async def end_trip(cls, app: Sanic, trip_id: UUID):
        """ Update trip id """
