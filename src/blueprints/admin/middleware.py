from sanic import Sanic
from sanic.request import Request
from sanic.response import json as sanjson
import jwt
import traceback, pprint

async def authorize(request: Request):
    """ Checks and authorize requests to admin endpoints """

    try:
        app = request.app

        pprint.pp(request.url)
        if 'auth' not in request.url:
            credentials = request.credentials
            print(f"Request credentials: {credentials}")

            if not credentials:
                return sanjson(
                    status=401,
                    body={
                        "info": "Unauthorized"
                        }
                    )
            
            payload = jwt.decode(credentials, app.ctx.pbkey, algorithm=["ES256K"])


    except jwt.exceptions.ExpiredSignatureError:
        return sanjson(
                status=400,
                body={
                    'info': 'Session expired'
                    }
                )
        pass

    except jwt.exceptions.InvalidTokenError:
        return sanjson(
                status=400,
                body={
                    "message": "Invalid credential"}
                )

    except Exception as e:
        print(traceback.format_exc(e))

        return sanjson(
            status=500,
            body={
                'message': "An error occurred when processing ypur request"
            }
        )


