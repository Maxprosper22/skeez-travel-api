from sanic import Request
from sanic.response import html as sanhtml, text as santext, json as sanjson

from uuid import UUID

async def index(request: Request):
    """ Media index page """

    return santext('Hello, world!, Welcome to the media domain.')

async def add_media(request: Request):
    """ Handle new media item """

    return santext('Hi, there! I handle media submissions.')

async def fetch_media(request: Request, id: UUID):
    """ Fetch media ID from database """

    return santext("Hello, heres's the media file you requested.")

async def delete_media(request: Request, mid: UUID):
    """ Delete media item from database """

    return santext("OK, it's done. I've deleted the file.")

