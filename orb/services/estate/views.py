from sanic import Request
from sanic.response import html as sanhtml, text as santext, json as sanjson

async def index(request: Request):
    """ Index route handler """
    
    app = request.app

    template = app.ctx.TemplateEnv.get_template('apps/estate/index.html')
    return sanhtml(template.render())

async def about(request: Request):
    """ About route handler """

    return santext("Hi, there. Want to know more about us? You've come are at the right place")
