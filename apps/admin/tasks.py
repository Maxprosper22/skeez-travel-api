from .signals import create_trip_success_signal, create_trip_failure_signal, trip_update_signal

async def create_trip_task(app):
    """ Task managing trip creation success signals """
    while True:
        await app.blueprints()

    await create_trip_success_signal()

async def create_trip_failure_task(app):
    """ Task managing trip creation success signals """

    await create_trip_success_signal()

async def create_trip_success_signal_task(app):
    """ Task managing trip creation success signals """

    await create_trip_success_signal()
