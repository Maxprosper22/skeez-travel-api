from sanic import Sanic
from sanic.response import html as sanhtml, text as santext, json as sanjson
from sanic.request import Request
from sanic.views import HTTPMethodView
from returns.maybe import Maybe, Some, Nothing

import pprint


async def view_trips(request: Request):
    """ Loads trip data """
    
    try:
        app = request.app
        pool = app.ctx.pool
        tripCtx = app.ctx.tripCtx
        tripService = tripCtx["TripService"]
        tripStatus = tripCtx['TripStatus']

        trip_array = tripService.trips

        match trip_array:
            case [*Trip] as trips:
                trip_cast = trips.copy()
                new_trip_array = []
                for trip in trip_cast:
                    trip = dict(trip)
                    trip['trip_id'] = trip['trip_id'].hex
                    trip['date'] = trip['date'].isoformat()
                    trip['status'] = trip['status'].value

                    new_trip_array.append(trip)
    
                return sanjson(
                    status=200,
                        body={
                        "trips": new_trip_array
                    }
                )
            case []:
                return sanjson(
                    status=200,
                    body={
                        "trips": []
                    }
                )
    except Exception as e:
        raise e

async def create_trip(request: Request):
    """ 
        Handler for creating new trips.

        Note;
            [1]: Update code to directly search db for trip that matches the given data rather than fetch all trips and then iteratung over them.
    """
 
    app = request.app       # The Sanic app instance
    print('Application blueprints: ', app.blueprints)
    # bp = app.bl
    pool = app.ctx.pool     # Database connection pool
    tripCtx = app.ctx.tripCtx
    tripService = tripCtx["TripService"]    # TripController class instance
    tripStatus = tripCtx['TripStatus']    # Trip status enum class

    Trip = tripCtx['Trip']     # Trip class object (not instance!)

    trip_data = request.json    # Form data submitted
    match trip_data:
        case None:
            return sanjson(
                status=400,
                body={
                    'message': "Bad request. No data provided"
                }
            )
        case {'destination': t_dest, 'date': t_date, 'capacity': t_cap, 'status': t_stat} if t_dest == None or t_date == None or t_cap == None or t_stat == None:
            return sanjson(
                status=400,
                body={
                    'message': 'Bad request. Missing required fields'
                }
            )
    
    match trip_data['status']:
        case 'pending':
            trip_data['status'] = tripStatus.PENDING
        case 'active':
            trip_data['status'] = tripStatus.ACTIVE

    print(trip_data)

    trips = tripService.trips 
    
    # See Note [1] for the code below

    if len(trips) >= 1:
         match trips:
            case [Trip as trip] if trip['destination']==trip_data['destination'] and trip['status']==tripStatus.PENDING and trip['date']==trip_data['date'] and len(trip['slot']) < trip['capacity']:
                # print(trip)
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

    save_trip = await tripService.create_trip(pool, new_trip)
    print("New Trip: ", save_trip)
            
    if not save_trip:
        return sanjson(
            status=404, 
            body={
                'status': 'bad',
                'msg': 'Trip not created'
            }
        )
        
    # Send signal to websocket hanlder to update trip listing 
    return sanjson(
        status = 201, 
        body = {
           'status': 'ok',
           'msg': 'Trip created',
           'data': {'trip': save_trip}
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


# class AdminAuthView(HTTPMethodView):
#     async def get(request: Request):
#         """ Admin authentication page handle """
#
#         app = request.app
#         pool = app.ctx.pool
#
#         template = app.ctx.template_env.get_template("admin/signin.html").render()
#
#         return sanhtml(template)

async def new_admin(request: Request, acct_id: str) -> sanjson:
    """ Create new admin accounts """

    try:
        app = request.app
        pool = app.ctx.pool
        passwordService = app.ctx.PasswordService
        accountCtx = app.ctx.accountCtx
        accountService = accountCtx["AccountService"]
        account = accountCtx["Account"]
        adminCtx = app.ctx.adminCtx

        match accountService.accounts:
            case [Account as acct] if acct.account_id.hex == acct_id:
                if acct.is_admin:
                    return sanjson(body={
                        "info": "User is already admin"
                    })

                new_admin = adminCtx["Admin"](
                    account=acct.account_id,
                    role=adminCtx["AdminRole"](adm_role)
                )
                acct.admin=new_admin

                async with pool.acquire() as conn:
                    await conn.execute("""INSERT INTO admin (admin_id, account_id, role, date) VALUES ($1, $2, $3, $4)""", new_admin.admin_id, new_admin.account_id, new_admin.role, new_admin.date)


            case _:
                return sanjson(
                    status=400,
                    body={
                        "info": "Unable to complete operation"
                    }
                )

    except Exception as e:
        raise e

async def signin(request: Request):
    """ Admin authentication endpoint """
    app = request.app
    pool = app.ctx.pool
    accountService = app.ctx.accountCtx["AccountService"]
    passwordService = app.ctx.PasswordService
    
    pprint.pp(accountService.accounts)
    auth_data = request.json
    print(auth_data)

    match auth_data:
        case {'email': email, 'password': password}:

            match accountService.accounts:
                case [Account as acc] if acc.email == email:
                    match acc.is_admin:
                        case True:
                            passCheck = await passwordService.verify(
                                password, acc.password
                            )
                            match passCheck:
                                case True:
                                    response = redirect("admin/dashboard")
                                    # Generate auth token
                                    account_details = dict(acc)
                                    account_details.pop('password')
                                    return sanjson(
                                        status=200,
                                        body={
                                            'info': 'Success',
                                            'data': {
                                                'account': account_details,
                                                'token': token
                                            }
                                    })

                                case False:
                                    return sanjson(
                                        status=401,
                                        body={
                                            'msg': 'Incorrect credentials'
                                        })
                        case False:
                            return sanjson(status=403, body={
                                'status': 'error',
                                'msg': 'Forbidden'
                            })
                case _:
                    return sanjson(
                        status=404,
                        body={
                            'message': 'Account not recognised'
                    })
        case _:
            return sanjson(
                status=400,
                body={
                    'msg': 'Bad request. Credentials not provided'
            })

async def admin_ws(request, ws):
    """ Admin websocket endpoint """


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
