import asyncio
from asyncio import PriorityQueue
from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel, Field, field_validator, model_validator
from sanic import Sanic
from asyncpg.pool import Pool
from uuid import UUID
from typing import Optional, Dict
from datetime import datetime, timedelta
# from returns.maybe import Maybe, maybe, Some, Nothing
import pprint

from src.models.trip import TripStatus, Trip

class EventType(Enum):
    REMINDER = "reminder"
    TRIP_START = "trip_start"

@dataclass(order=True)
class TripEvent:
    event_date: datetime
    event_type: EventType
    trip: Trip


class TripService:

    def __init__(self):
        self.trips: Dict[UUID, Trip] = {}
        self.queue = PriorityQueue()
        self.pool: Pool = None
        self.reminder_offset = timedelta(days=1)
        self.running: bool = False


    async def create_table(self, pool: Pool) -> None:
        """ Create a table for storing trips in database """

        try:
            async with pool.acquire() as conn:
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS trips (
                        trip_id UUID PRIMARY KEY,
                        destination TEXT NOT NULL,
                        capacity INTEGER NOT NULL,
                        status TEXT NOT NULL,
                        date TIMESTAMP NOT NULL
                    )
                """)
        except Exception as e:
            raise e
    
    async def initialise(self, pool: Pool) -> None:
        """
            Fetches all trips from database and populate `self.trips`. This method is to be run on server start up.

            Note: To access trips use `self.trips`
        """
        self.pool = pool

        # print("Checking trip status values")
        # print(TripStatus.PENDING.value)

        async with pool.acquire() as conn:
            trip_records = await conn.fetch("SELECT * FROM trips WHERE status IN ($1, $2)", TripStatus.PENDING.value, TripStatus.ACTIVE.value)  # Retrieve trips waiting to commence
    
        if trip_records:
            print("Checking trip records:")
            pprint.pp(trip_records)
            trips = [dict(trip) for trip in trip_records]
            for trip_item in trips:
                # trip['status'] = TripStatus(trip['status'])
                trip = Trip(
                    trip_id = trip_item["trip_id"],
                    destination = trip_item["destination"],
                    capacity = trip_item["capacity"],
                    status = TripStatus(trip_item["status"]),
                    date = trip_item["date"]
                )
                await self._add_trip_events(trip)
                 
    async def _add_trip_events(self, trip: Trip):
        """ Add reminfer and trip start events to queue """
        self.trips[trip.trip_id] = trip
        # Add reminder event (1 day before)
        reminder_time = trip.date - self.reminder_offset
        if reminder_time > datetime.now():
            await self.queue.put(TripEvent(reminder_time, EventType.REMINDER, trip))
        # Add trip start event
        await self.queue.put(TripEvent(trip.date, EventType.TRIP_START, trip))



    async def create_trip(self, pool: Pool, trip: Trip) -> Optional[dict]:
        """ Create a trip instance """
        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO trips (
                    trip_id,
                    destination, 
                    capacity,
                    status,
                    date
                ) VALUES ($1, $2, $3, $4, $5, $6)
            """,
                trip.trip_id, trip.destination, trip.capacity, trip.status.value, trip.date
            )

            await self._add_trip_events(trip)
        
            
    async def update_trip(self, pool: Pool, tripid: UUID, new_start_date: datetime):
        """ Updates trip start date """
        if tripid in self.trips:
            trip = self.trips[tripid]
            trip.date = new_start_date
            # Update database
            async with pool.acquire() as conn:
                await conn.execute("UPDATE trips SET date = $1 WHERE trip_id = $2", new_start_date, tripid)

            # Re-add events to queue
            await self._add_trip_events(trip)

    async def cancel_trip(self, pool: Pool, tripid: UUID) -> Optional[Trip]:
        """ Cancels trip """
        if tripid in self.trips:
            del self.trips[tripid]
            async with pool.acquire() as conn:
                await conn.execute("UPDATE trips SET status = $1 WHERE trip_id=$2", TripStatus.CANCELLED, tripid)


    async def complete_trip(self, pool: Pool, tripid: UUID):
        """ Marks a trip as complete """
        
        if tripid in self.trips and self.trips[tripid].status == TripStatus.ACTIVE:
            trip = self.trips[tripid]
            await self.update_trip_status(trip, TripStatus.COMPLETED)
            await self.send_notification(trip, "completed")
            # Optionally remove trip
            del self.trips[tripid]
        else:
            raise ValueError("Trip {tripid} is not active or or does not exist")

    async def update_trip_status(self, pool: Pool, trip: Trip, status: TripStatus):
        """
            Update trip (trip_id) status to (status). Status may be one of the following ['pending', 'active', 'cancelled', 'complete']
        """
        try:
            async with pool.acquire() as conn:
                modded_trip = await conn.execute("""
                    UPDATE trips SET status=$1 WHERE trip_id=$2
                """, status, trip_id)

            trip.status = status

        except Exception as e:
            raise e        

    async def send_notification(self, trip: Trip, event_type: EventType):
        """ Send notifications based on trip events """

        if event_type == EventType.Reminder:
            print(f"Reminder: Trip {trip.tripid} starts in 1 day at {trip.start_date}")
        elif event_type == EventType.TRIP_START:
            print(f"Notification: Trip {trip.tripid} has started at {trip.start_date}")

    async def run_trips(self):
        """
            Run all trips in with pending and active statuses in self.trips. Runs on server startup.
        """
        try:
            while True:
                # Get next event
                trip_event = self.queue.get()
                current_time = datetime.now()
                event_time = trip_event.event_time
                trip = trip_event.trip

                # Sleep until time for event
                delay = (event_type - current_time).total_seconds()
                if delay > 0:
                    asyncio.sleep(delay)

                # Process all events with the same time
                events_to_process = [trip_event]

                # Pick at the queue to for events with the same time
                while not self.queue.empty():
                    next_event = await self.queue.get()
                    if next_event.event_time <= event_time:
                        events_to_process.append(next_event)
                    else:
                        await self.queue.put(next_event)
                        break

                # Process all collected events
                for event in events_to_process:
                    trip = event.trip
                    if trip.trip_id not in self.trips:
                        continue  # Skip if trip was cancelled or updated
                    if event.event_type == EventType.REMINDER:
                        await self.send_notification(trip, EventType.REMINDER)
                    elif event.event_type == EventType.TRIP_START and trip.status == TripStatus.PENDING:
                        await self.update_trip_status(trip, TripStatus.ACTIVE)
                    await self.send_notification(trip, EventType.TRIP_START)

                # Mark all processed events as done
                for _ in events_to_process:
                    await self.queue.taskdone()

        except Exception as e:
            raise e


    # @classmethod
    # async def pending_trip_task(cls, app: Sanic, trip: Trip) -> None:
    #     """ A method tracks the approaching date of a trip """
    #     try:
    #         count_down = trip.date - datetime.now()
    #         if datetime.now() >= trip.date:
    #             """
    #                 - Send alert to admin and users about the start of trip 
    #                 - Change trip status to active
    #             """
    #             cls.update_trip_status(
    #                 cls.pool,
    #                 trip=trip.trip_id,
    #                 status=TripStatus.ACTIVE
    #             )
    #             cls.app.cancel_task(name=f"trip-{trip.trip_id.hex}")
    #
    #         if count_down.days != 0 and count_down.days <= 3:
    #
    #             await asyncio.sleep(86400) # Sleep for 24 hours and check again
    #             # Send email and sms
    #             print(f"Hello there! Your trip to {trip.destination} is 5 days away. How's your packing going?")
    #
    #     except Exception as e:
    #         raise e
    #

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

