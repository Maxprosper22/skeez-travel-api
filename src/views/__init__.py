from sanic import Request
from sanic.response import html as sanhtml, text as santext, json as sanjson, redirect

import traceback

async def index(request: Request):
    """ Index route handler """
    try:
        app = request.app
        template = app.ctx.template_env.get_template('main/index.html')
        render = template.render()

        return sanhtml(render)
    except Exception as e:
        print(traceback.format_exc(e))

async def notifications_handler(request: Request):
    app =request.app
    
    return santext('Manage notifications over ere.')

async def account_handler(request: Request):
    app = request.app

    return santext('Here you manage your account info')

async def signin(request: Request) -> sanhtml:
    """
    Sign in handler
    """
    try:

        app = request.app
        pool = app.ctx.pool
        template = app.ctx.template_env.get_template('main/signin.html')
        
        if request.method == 'get':

            render = template.render()
            return sanhtml(render)

        elif request.method == 'post':
            
            # Get form data
            formData = request.body
            formEmail = formData.get('email')
            formPassword = formData.get('password')

    except Exception as e:
        raise e

async def destinations_handler(request: Request) -> sanhtml:
    """
        Returns a list of a destinations
    """

    try:
        app = request.app
        pool = app.ctx.pool
        template = app.ctx.template_env.get_template('main/destinations.html')
        render = template.render()

        return sanhtml(render)
    except Exception as e:
        raise e
        
async def booking_handler(request: Request):
    """ Handle ride booking """

    try:
        app = request.app
        pool = app.ctx.pool
        booker = BookManager()

    except Exception as e:
        raise e

async def signin(request: Request):
    pass

async def signup(request: Request):
    pass

async def dashboard(request: Request):
    return redirect('/')

