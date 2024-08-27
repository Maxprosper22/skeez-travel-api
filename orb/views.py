from sanic import Request
from sanic.response import html as sanhtml, text as santext, json as sanjson, redirect

import traceback

async def index(request: Request):
    """ Index route handler """
    try:
        app = request.app
        template = app.ctx.TemplateEnv.get_template('index.html')
        render = template.render()

        return sanhtml(render)
    except Exception as e:
        print(traceback.format_exc(e))

async def home(request: Request):
    """ Home route handler """
    try:
        app = request.app
        template = app.ctx.TemplateEnv.get_template('market.html')
        render = template.render()

        return sanhtml(render)

    except Exception as e:
        print(traceback.format_exc(e))

async def timeline(request: Request):
    app = request.app

    return santext("Hello, fetch your timeline here")

async def post(request: Request, postid):
    app = request.app
    template = app.ctx.TemplateEnv.get_template('thread.html')
    render = template.render()

    return sanhtml(render)
