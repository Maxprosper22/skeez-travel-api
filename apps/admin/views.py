from sanic import Sanic
from sanic.response import html as sanhtml, text as santext, json as sanjson
from sanic.request import Request
from sanic.views import HTTPMethodView
from returns.maybe import Maybe, Some, Nothing

async def dashboard(request: Request):
    """ Admin dashboard """

    app = request.app
    pool = app.ctx.pool
    templateEnv = app.ctx.template_env
    
    print(type(templateEnv))
    print(templateEnv.loader.__dir__())
    print(templateEnv.loader.list_templates)

    template = templateEnv.get_template("admin/dashboard.html").render()

    return sanhtml(template)

async def view_trips(request: Request):
    """ Loads trip data """

    app = request.app
    pool = app.ctx.pool
    tripCtx = app.ctx.tripCtx
    tripStatus = tripCtx['tripStatus']
    templateEnv = app.ctx.template_env

    trips = await tripCtx['fetch_trips'](pool)
    template = templateEnv.get_template("admin/trip-board.html")

    match trips:
        case Some(trips):
            return sanhtml(
            template.render(
                trips=trips,
                trip_status=tripStatus
            ))
        case Nothing:
            return sanhtml(template.render(
                trip_status=tripStatus
                ))

async def create_trip(request: Request):
    """ Create new trip """
    
    app = request.app       # The Sanic app instance
    print('Application blueprints: ', app.blueprints)
    # bp = app.bl
    pool = app.ctx.pool     # Database connection pool
    tripCtx = app.ctx.tripCtx    # Dictionary continaing trip context objects
    tripStatus = tripCtx['tripStatus']    # Trip status enum class
    fetchTrips = tripCtx['fetch_trips']   # Finction to fetch trips from db
    tripStatus = tripCtx['tripStatus']

    Trip = tripCtx['trip']     # Trip class object (not instance!)

    trip_data = request.json    # Form data submitted
    print(trip_data)
    match trip_data['status']:
        case 'pending':
            trip_data['status'] = tripStatus.PENDING
        case 'active':
            trip_data['status'] = tripStatus.ACTIVE

    print(trip_data)

    trips = await fetchTrips(pool)

    if trips:
        for trip in trips:
            if trip['destination']==trip_data['destination'] and trip['status']==tripStatus.PENDING and trip['date']==trip_data['date'] and len(trip['slot']) < trip['capacity']:
                print(trip)
                # await 

                return sanjson(
                    status=403,
                    body={
                        'status': 'err',
                        "msg": f"Unable to create trip to '{trip_data.destination}'. Existing trip(s) with free slots found"
                })

    new_trip = Trip(
            destination=trip_data['destination'],
            date=trip_data['date'],
            status=trip_data['status'],
            capacity=trip_data['capacity']
    )
    print(new_trip)

    save_trip = await tripCtx['create_trip'](pool, new_trip)
            
    if not save_trip:
        return sanjson(
            status=404, 
            body={
                'status': 'bad',
                'msg': 'Trip not created'
            }
        )
        
    # Send signal to websocket hablder to update trip listing 
    return sanjson(
        status = 201, 
        body = {
           'status': 'ok', 
            'msg': 'Trip created'
        }
    )
           

async def start_trip(request: Request, trip_id: str):
    """
        Endpoint to begin a specific trip
        Method: Patch
    """

async def end_trip(request: Request, trip_id: str):
    """ 
        Handles trip completion
        Method: Get
    """

async def cancel_trip(request: Request, trip_id: str):
    """ 
        Cancels trip before completion
        Method: Put
    """
    

class TripView(HTTPMethodView):
    async def get(self, request: Request, trip_id: str):
        """ Fetch a specific trip """

    async def post(self, request: Request):
        """ Create a new trip """

    async def delete(self, request: Request, trip_id: str):
        """ Delete a trip """

    async def patch(self, request: Request, trip_id, **kwargs):
        """ Update trip data """

    async def put(self, request: Request):
        """ Update trip """



class AdminAuthView(HTTPMethodView):
    async def get(request: Request):
        """ Admin authentication page handle """

        app = request.app
        pool = app.ctx.pool

        template = app.ctx.template_env.get_template("admin/signin.html").render()

        return sanhtml(template)

    async def post(self, request: Request):
        """ Admin authentication endpoint """
        app = request.app
        pool = app.ctx.pool
        password_manager = app.ctx.PasswordManager()

        auth_data = request.json
        match auth_data:
            case {'email': email, 'password': password}:
                async with pool.acquire() as conn:
                    account_rec = await conn.fetchrow()

                if account_rec:
                    account = dict(account_rec)
                    match account.is_admin:
                        case True:
                            passCheck = await password_manager.verify(password, account.password)
                            match passCheck:
                                case True:
                                    response = redirect("admin/dashboard")
                                    # Add cookies here
                                    return response

                                case False:
                                    return sanjson(status=401, body={
                                        'msg': 'Incorrect credentials'
                                    })
                        case False:
                            return sanjson(status=403, body={
                                'status': 'error',
                                'msg': 'Forbidden'
                            })
                else:
                    return sanjson(status=404, body={
                        'message': 'Account not recognised'
                        })
            case _:
                return sanjson(status=400, body={
                    'msg': 'Bad request. Credentials not provided'
                    })

async def admin_ws(request, ws):
    """ Admin websocket endpoint """
