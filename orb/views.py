from sanic import Request
from sanic.response import html as sanhtml, text as santext, json as sanjson, redirect

import traceback

async def index(request: Request):
    """ Index route handler """

    return santext('Index page')

async def home(request: Request):
    """ Home route handler """
    try:
        app = request.app
        template = app.ctx.TemplateEnv.get_template('home.html')
        render = template.render()

        return sanhtml(render)

    except Exception as e:
        print(traceback.format_exc(e))
