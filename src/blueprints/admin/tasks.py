from .signals import create_trip_success, create_trip_failure, trip_update_signal

from uuid import UUID
from mailbridge import MailBridge
from datetime import datetime
import asyncio


async def trip_task(app: Sanic, tripid: UUID):
    """ Function that monitors trip date. Fetches trip data and sends emails to associated users """
    try:
        app = app
        tripService = app.ctx.tripCtx['TripService']

        trip = await tripService.fetch_trip(tripid=tripid)
        
        for account in trip.accounts:
            mailer = MailBridge(
                provider='smtp',
                host='mail.zoho.com',
                port=587,
                username=app.ctx.mailConfig['ADMIN'],
                password=app.ctx.mailConfig['PASSWORD'],
                use_ssl=True,  # For port 465
                from_email=app.ctx.mailConfig['ADMIN']
            )
            
            if datetine.now() != trip.date:
                # eta = trip.date - datetime.now()
                response = mailer.send(
                    to=account.email,
                    subject="Trip Update",
                    body=f"Your trip to {trip.destination.name} starts in {eta.days}:{eta.hours}. View at {app.config.CLIENT_ÚRL}"
                )
            for client in app.SSEClients:
                client[0].send(f"event: alert\ndata: json.dumps('type': 'start', 'message': 'Trip Started', 'tripid': {trip.tripid})")

                return

            response = mailer.send(
                to=account.email,
                subject="Trip Update",
                body=f"Your trip to {trip.destination.name} is today. View at {app.config.CLIENT_ÚRL}"
            )

        for client in app.SSEClients:
            client[0].send(f"event: alert\ndata: json.dumps('type': 'start', 'message': 'Trip Started', 'tripid': {trip.tripid})")

    except Exception as e:
        raise e


async def trip_listener(event):
    """ Listens for events from the Schedule """


