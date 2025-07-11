from sanic import Sanic

async def setup_accounts(app: Sanic):
    """ Set up account management """

    # app.ctx.AccountModel = Account
    # app.ctx.accountCtx = {
    #     "accountModel": Account,
    #     "accountController": AccountController()
    # }

    # Create new accounts table if it doesn't exist
    # await app.ctx.accountCtx["accountController"].create_table(pool=app.ctx.pool)
    
    # Retrieve and populate Accounts array of the AccountController
    # await app.ctx.accountCtx["accountController"].populate_accounts(app.ctx.pool)
