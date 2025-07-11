from sanic import Sanic
from sanic.request import Request
from sanic.response import html as sanhtml, json as sanjson

from uuid import UUID

async def account_info(request: Request, account_id: str) -> sanjson:
    """ Retrieve account information """
    try:
        if not account_id:
            return sanjson(
                    status=400,
                    body={
                        'info': 'Missing a required field'
                        }
                    )

        app = request.app
        pool = app.ctx.pool
        accountModel = app.ctx.accountCtx["Account"]
        accountService = app.ctx.accountCtx["AccountService"]

        match accountService.accounts:
            case [accountModel() as acctModel] if acctModel.account_id.hex == account_id:
                account_data = dict(acctModel)
                account_data.pop("password")

                return sanjson(
                        body={
                            "data": account_data
                            }
                        )

            case _:
                return sanjson(
                        status=404,
                        body={
                            "info": "No data found"
                            }
                        )

    except Exception as e:
        raise e

async def account_trips(request: Request, account_id: str):
    """ Retrieve accoint related trips """

async def account_payments(request: Request, account_id: str):
    """ Retrieve account payment history """


