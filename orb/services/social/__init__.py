from sanic import Sanic

async def app_factory() -> Sanic:
    """ Application factory """

    app = Sanic("OrbSocial")

    app.static('/static', '/assets')
    
    @app.listener('before_server_start')
    async def server_setup(app, loop):
        """ Setup server configuration """
        pass

    return app
