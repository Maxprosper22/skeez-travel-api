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

async def timeline(request: Request):
    app = request.app

    return santext("Hello, fetch your timeline here")

async def post(request: Request, postid):
    app = request.app
    template = app.ctx.TemplateEnv.get_template('thread.html')
    render = template.render()

    return sanhtml(render)


async def createpost(request: Request):
    app = request.app

    return santext('Create new posts here.')

async def notifications_handler(request: Request):
    app =request.app
    
    return santext('Manage notifications over ere.')

async def chats_handler(request: Request):
    app = request.app

    return santext('Chat with your contacts here')

async def profile_handler(request: Request):
    app = request.app

    return santext('Here you manage your account info')
