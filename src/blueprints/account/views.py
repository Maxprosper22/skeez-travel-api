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

async def signin(request: Request):
    """ Handle user authentication """
    try:
        app = request.app
        pool = app.ctx.pool
        accountCtx = app.ctx.accountCtx
        Account = accountCtx["Account"]
        accountService = accountCtx["AccountService"]
        passwordService = app.ctx.PasswordService

        auth_data = request.json

        match auth_data:
            case None:
                return sanjson(status=400, body={
                    "info": "Invalid credentials"
                })

            case {"email": email, "password": password}:
                if not email:
                    return sanjson(status=400, body={
                        "info": "Missing required field - Email"
                    })
                if not password:
                    return sanjson(status=400, body={
                        "info": "Missing required field - Password"
                    })

                match accountService.accounts:
                    case [Account(email=email) as acct]:
                        passCheck = passwordService.verify(password, acct.password)

                        if not passCheck:
                            return sanjson(status=400, body={
                                "info": "Invalid credentials"
                            })

                        user_data = dict(acct)
                        user_data.pop("password")

                    case _:
                        return sanjson(status=404, body={
                            "info": "Invalid credentials"
                        })

    except Exception as e:
        raise e

async def signup(request: Request):
    """ Endpoint for handling account creation """
    try:
        app = request.app
        pool = app.ctx.pool
        pvkey = app.ctx.pvkey

        accountCtx = app.ctx.accountCtx
        Account = accountCtx["Account"]
        accountService = accountCtx["AccountService"]

        passwordService = app.ctx.PasswordService

        tokenCtx = app.ctx.tokenCtx
        Token = tokenCtx["Token"]
        tokenType = tokenCtx["TokenType"]
        tokenService = tokenCtx["Service"]

        form_data = request.json

        match form_data:
            case None:
                return sanjson(status=400, body={'info': 'Bad request'})

            case {'email': email, 'password': password, 'password2': password2, 'phone': phonenumber, 'firstname': firstname, 'lastname': lastname, 'othername': othername}:
                if not email:
                    return sanjson(status=400, body={'info': 'Misssing required field: email'})

                if not password:
                    return sanjson(status=400, body={'info': 'Misssing required field: password'})

                if not password2:
                    return sanjson(status=400, body={'info': 'Misssing required field: password2'})

                if not phonenumber:
                    return sanjson(status=400, body={'info': 'Misssing required field: phone'})

                if not firstname:
                    return sanjson(status=400, body={'info': 'Misssing required field: firstname'})
                if not lastname:
                    return sanjson(status=400, body={'info': 'Misssing required field: lastname'})

                if password != password2:
                    return sanjson(status=400, body={'info': 'Passwords do not match'})

                match accountService.accounts:
                    case Account(email=email) as acct:
                        return sanjson(status=409, body={'info': 'This email is already registered'})
                    case None:
                        new_account_model = Account(
                            email=email, 
                            phone_number=phonenumber,
                            password=passwordService.make_hash(password),
                            firstname=firstname,
                            lastname=lastname,
                            othername=othername
                        )
                        new_account = await accountService.create_account(pool, new_account_model)
                        account_dict = dict(new_account)
                        account_dict.pop('password')

                        newToken = Token(
                            account_id = account_id["account_id"],
                            valid = True,
                            token_type = tokenType.AUTH
                        )
                        gen_token = await tokenService.generate_token(pool, newToken, pvkey)
                        newToken.signature = gen_token.split('.')[-1]
                        
                        await tokenService.store_token(pool, newToken)

                        account_dict["account_id"] = account_dict["account_id"].hex

                        return sanjson(status=201, body={
                            'info': 'Account created',
                            'data': account_dict,
                            'token': gen_token
                        })

    except Exception as e:
        raise e

async def account_trips(request: Request, account_id: str):
    """ Retrieve accoint related trips """

async def account_payments(request: Request, account_id: str):
    """ Retrieve account payment history """


