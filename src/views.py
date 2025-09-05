from sanic import Sanic, Blueprint
from sanic.request import Request
from sanic.response import html as sanhtml, json as sanjson, text as santext, file as sanfile, HTTPResponse
from sanic.log import logger

import pprint, json, asyncio
from uuid import UUID

from src.models.sse import BaseField, Event, Data, ID, Retry, Heartbeat, message

async def index(request: Request, path: str):
    app = request.app
    pool = app.ctx.pool
    templateEnv = app.ctx.template_env

    user = request.ctx.user
    #
    # template = templateEnv.get_template('main/index.html').render(user=user)
    #
    # return sanhtml(template)

    return sanhtml(app.config.DIST_DIR / "index.html")
 
async def view_destinations(request: Request):
    try:
        app = request.app
        pool = app.ctx.pool

        tripCtx = app.ctx.tripCtx
        tripService = tripCtx['TripService']

        destinations = await tripService.fetch_destinations(pool)
        for destination in destinations:
            destination['destination_id'] = destination['destination_id'].hex

        return sanjson(body={'data': destinations if destinations else None})
    except Exception as e:
        raise e
    
async def view_trips(request: Request):
    """ 
        View available trips
        Method: Get
    """

    app = request.app
    pool = app.ctx.pool

    templateEnv = app.ctx.template_env
    template = templateEnv.get_template('main/trips.html')

    user = request.ctx.user

    rendered_template = template.render(user=user)
    return sanhtml(rendered_template)

async def fetch_trips(request: Request):
    """ Api endpoint for retrieving trips """

    app = request.app
    pool = app.ctx.pool

    tripCtx = app.ctx.tripCtx
    Trip = tripCtx['Trip']
    tripStatus = tripCtx['TripStatus']
    tripService = tripCtx['TripService']

    trips = await tripService.fetch(pool=pool)
    
    if not trips:
        # rendered_template = template.render(trips=[])
        return sanjson(body={'info': 'No trip available'})

    all_trips = []
    
    for trip in trips:
        # tripItem = trip.model_dump()

        trip['trip_id'] = trip['trip_id'].hex
        trip['destination_id'] = trip['destination_id'].hex
        trip['destination']['destination_id'] = trip['destination']['destination_id'].hex

        trip['destination']['price'] = int(trip['destination']['price'])
        # trip['status'] = trip['status'].value
        trip['date'] = trip['date'].isoformat()

        for slot in trip['slots']:
            slot['account_id'] = slot['account_id'].hex
            slot['join_date'] = slot['join_date'].isoformat()
            slot.pop('password')

        all_trips.append(trip)

    return sanjson(body={'data': all_trips})

async def view_trip(request: Request, tripid: str):
    """ 
        Retrieve data for a specific trip
        Method: Get
    """
    
    app = request.app
    pool = app.ctx.pool

    user = request.ctx.user

    templateEnv = app.ctx.template_env
    template = templateEnv.get_template('main/trip.html')

    tripCtx = app.ctx.tripCtx
    tripService = tripCtx['TripService']
    
    if tripid == None:
        return sanjson(401, {"info": "Invalid operation. No trip id provided"})  # A tuple containing a status code and a message: (status, message)

    tripId = UUID(hex=tripid)
    tripData = await tripService.fetch_trip(pool, tripId)
    pprint.pp(tripData)
    if not tripData:
        return sanjson(body={'info': 'Trip not found'})

    tripData = tripData.model_dump()
    tripData['trip_id'] = tripData['trip_id'].hex
    tripData['destination']['destination_id'] = tripData['destination']['destination_id'].hex
    tripData['status'] = tripData['status'].value
    tripData['date'] = tripData['date'].isoformat()
    
    if tripData['slots']:
        for slot in tripData['slots']:
            slot.pop('password')
            slot['account_id'] = slot['account_id'].hex
            slot['join_date'] = slot['join_date'].isoformat()
    
    # pprint.pp(f"Array of trips: {tripData}")
    # passengers = 
    
    return sanjson(body={'data': tripData})

async def trip_sse(request: Request):
    """Pushes updates to clients via SSE."""
    try:
        app = request.app
        pool = app.ctx.pool

        tripCtx = app.ctx.tripCtx
        Trip = tripCtx['Trip']
        tripStatus = tripCtx['TripStatus']
        tripService = tripCtx['TripService']

        pubsub = app.ctx.pubsub
        publisher = app.ctx.Publisher
        sse_subscriber = app.ctx.SSESubscriber
        clientSubscription = app.ctx.clientSubscription

        user = request.ctx.user
        
        # Get trip IDs from query parameters
        trip_ids = request.args.getlist("trip_id") or []
        # Validate UUIDs
        try:
            trip_ids_set = {str(uuid.UUID(tid)) for tid in trip_ids} if trip_ids else set()
        except ValueError:
            return response.json({"error": "Invalid UUID in trip_id"}, status=400)

        # Default to all trips if none specified
        if not trip_ids_set:
            trips = await tripService.fetch(pool=pool)  # Assume async method
            trip_ids_set = {trip["trip_id"] for trip in trips}
        
        # Create a response with streaming enabled
        headers = {
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
        resp = await request.respond(
            headers=headers,
            content_type="text/event-stream"
        )

        # Register client subscription
        # client = clientSubscription(stream=resp, trip_ids=trip_ids_set)
        # pubsub.subscribe(client, trip_ids_set)

        client = sse_subscriber(accountid=user['account_id'] if user else None, stream=resp)
        publisher.channels["sse"].subscribe(client)

        # Send initial welcome message
        await resp.send(f"event: welcome\ndata: {json.dumps({'message': 'Connected to trip updates'})}\n\n")

        # Keep connection alive with periodic keep-alive messages
        try:
            while True:
                await resp.send(":\n\n")  # Keep-alive
                await asyncio.sleep(15)  # Every 15 seconds
        except asyncio.CancelledError:
            # Client disconnected
            publisher.channels['sse'].unsubscribe(client)
            logger.info("Client disconnected")
        except Exception as e:
            publisher.channels['sse'].unsubscribe(client)
            logger.error(f"Unexpected error in SSE stream: {e}")
        finally:
            await resp.eof()  # Ensure stream is closed

        pprint(f'Publisher: {publisher}')

    except Exception as e:
        logger.error(f"Error in trip_sse: {e}")
        raise e

async def book(request: Request, tripid: str):
    """ 
        Register a passenger for a trip
        Method: Post
    """
    try:
        app = request.app
        pool = app.ctx.pool

        paystackConfig = app.ctx.PaystackConfig

        httpxClient = app.ctx.httpxClient

        accountCtx = app.ctx.accountCtx
        accountService = accountCtx['AccountService']

        tripCtx = app.ctx.tripCtx
        Trip = tripCtx['Trip']
        tripStatus = tripCtx['TripStatus']
        tripService = tripCtx['TripService']

        booking_info = request.json

        trip_data = await tripService.fetch_trip(pool=pool, tripid=tripid)
        if not trip_data:
            return sanjson(status=404, body={'info': 'Trip not found'})

        if len(trip_data.slots) >= trip_data.capacity:
            return sanjson(status=400, body={'info': 'Trip at full capacity'})

        trip = await tripService.fetch_trip(pool=pool, tripid=booking_info['tripid'])

        if not trip:
            return sanjson(status=404, body={'info': 'Trip not found'})

        user = await accountService.fetch_user(pool=pool, accountid=UUID(hex=trip_data['accountid']))
        if not user:
            return sanjson(status=403, body={'info': 'Forbidden'})

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {paystackConfig['SECRET_KEY']}"
        }
        payload = {'email': user['email'], 'amount': trip.destination.price}
        async with httpxClient.post('api.paystack.co/transaction/initialize', data=payload, headers=headers) as resp:
            pprint.pp(resp)
            response = resp.json()

        async with pool.acquire() as conn:
            ticket = await conn.fetchrow("SELECT * FROM tickets WHERE trip_id=$1 AND account_id=$2", booking_info["tripid"], booking_info["accountid"])

        if ticket:
            return sanjson(400, body={'info': 'You already have a reservation'})

        await tripService.book(pool, UUID(booking_info['tripid']), UUID(booking_info['accountid']))

        return sanjson(status=201, body={'info': 'Successfully booked trip', 'data': True})

    except Exception as e:
        raise e

async def unbook(request: Request, tripid: str):
    """
        Remove a passenger from the list of passengers
        Method: Patch
    """
    try:
        app = request.app
        pool = app.ctx.pool
        tripCtx = app.ctx.tripCtx
        tripService = tripCtx['TripService']

        unbook_data = request.json

        async with pool.acquire() as conn:
            ticket = await conn.fetchrow("SELECT * FROM tickets WHERE trip_id=$1 AND account_id=$2", unbook_data['tripid'], unbook_data['accountid'])

        if not ticket:
            return sanjson(status=400, body={'info': 'No reservation found'})

        unbook_report = await tripService.unbook(pool=pool, tripid=unbook_data['tripid'], accountid=unbook_data['accountid'])

        if unbook_report == "FAILURE":
            return sanjson(status=500, body={
                'info': 'An error occurred while processing request'
                })
        return sanjson(status=200, body={'info': "Operation SUCCESS"})

    except Exception as e:
        raise e
