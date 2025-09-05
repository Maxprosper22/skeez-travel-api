from sanic import Sanic

from .views import fetch_trips, fetch_trip, book, unbook

async def router(app: Sanic) -> None:
    """ Set up trip router """

    app.add_route(fetch_trips, '/trips', methods=['GET'])
    app.add_route(fetch_trip, '/trip/<tripid>', methods=['GET'])
    app.add_route(book, '/trip/<tripid>/book', methods=['GET', 'POST'])
    app.add_route(unbook, '/trip/<tripid>/unbook', methods=['POST'])
