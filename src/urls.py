from sanic import Sanic

from src.views import index, view_trips, trip_sse, fetch_trips, view_trip, book, unbook, view_destinations, payment_webhook


async def router(app: Sanic) -> None:
    """ Set up trip router """

    # app.add_route(index, '/<path:path>', methods=['GET'])
    app.add_route(view_destinations, '/destinations', methods=['GET'])
    app.add_route(fetch_trips, '/api/trips', methods=['GET'])
    app.add_route(view_trips, '/trips', methods=['GET'])
    app.add_route(trip_sse, '/sse/<userid:strorempty>', methods=['GET'])
    app.add_route(view_trip, '/trip/<tripid>', methods=['GET'])
    app.add_route(book, '/trip/<tripid>/book/', methods=['POST'])
    app.add_route(book, '/trip/<tripid>/book/complete', methods=['GET', 'POST'])
    app.add_route(book, '/trip/<tripid>/book/cancel', methods=['GET', 'POST'])
    app.add_route(unbook, '/trip/<tripid>/unbook', methods=['POST'])
    app.add_route(payment_webhook, '/payment/webhook', methods=['POST'])
