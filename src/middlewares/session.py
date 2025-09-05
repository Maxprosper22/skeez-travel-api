import jwt
from sanic.request import Request

import pprint

async def session(request: Request):
    """ Handles session """

    try:
        app = request.app
        pool = app.ctx.pool

        accountCtx = app.ctx.accountCtx
        Account = accountCtx['Account']
        accountService = accountCtx['AccountService']

        tokenCtx = app.ctx.tokenCtx
        Token = tokenCtx['Token']
        tokenType = tokenCtx['TokenType']
        tokenService = tokenCtx['TokenService']

        session_cookie = request.cookies.get("session")
        if session_cookie:

            token_sig = session_cookie.split["."][-1]
            tokenCheck = await tokenService.check_token(pool=pool, signature=token_sig)
            if tokenCheck:
                account_data = await accountService.fetch_user(pool=pool, accountid=token.account_id)
                account_data.pop('password')
                # pprint.pp(account_data)
                request.ctx.user = account_data
            else:
                request.ctx.user = None
        else:
            request.ctx.user = None

    except Exception as e:
        raise e
