from sanic import Sanic
from sanic.request import Request
from sanic.response import html as sanhtml, json as sanjson
from sanic.views import HTTPMethodView

from uuid import UUID
import pprint, traceback
import asyncio

from pydantic_extra_types.phone_numbers import PhoneNumber

async def account_info(request: Request, account_id: str) -> sanjson:
    """ Retrieve account information """
    try:
        if not account_id:
            return sanjson(
                status=400,
                body={
                    'info': 'Missing a required field'
            })

        app = request.app
        pool = app.ctx.pool
        accountModel = app.ctx.accountCtx["Account"]
        accountService = app.ctx.accountCtx["AccountService"]

        match accountService.accounts:
            case [accountModel() as acctModel] if acctModel.account_id.hex == account_id:
                account_data = dict(acctModel)
                account_data.pop("password")

                return sanjson(body={"data": account_data})

            case _:
                return sanjson(
                    status=404,
                    body={
                        "info": "No data found"
                })

    except Exception as e:
        raise e

async def signout(request: Request):
    """ Handle user authentication """
    try:
        app = request.app
        pool = app.ctx.pool
        token = request.token
        pprint.pp(f"Auth token: {token}")

        tokenCtx = app.ctx.tokenCtx
        Token = tokenCtx['Token']
        tokenService = tokenCtx['TokenService']

        if not token:
            return sanjson(status=400, body={'info': 'Bad request'})

        tk_sig = token.split('.')[-1]
        retrieve_tk = await tokenService.fetch_token(pool=pool, signature=tk_sig)

        if not retrieve_tk:
            return sanjson(status=400, body={'info': 'Bad or invalid token'})

        token_res = await tokenService.invalidate_token(pool=pool, signature=tk_sig)
        
        if token_res.valid:
            return sanjson(status=500, body={'info': 'An error occurred during operation'})

        return sanjson(status=200, body={'info': 'Successfully logged out', 'authenticated': False})

    except Exception as e:
        raise e
    
async def signin(request: Request):
    """ Handle user authentication """
    try:
        app = request.app
        pool = app.ctx.pool
        pvkey = app.ctx.pvkey

        accountCtx = app.ctx.accountCtx
        Account = accountCtx["Account"]
        accountService = accountCtx["AccountService"]

        adminCtx = app.ctx.adminCtx
        Admin = adminCtx['Admin']
        adminService = adminCtx['AdminService']

        passwordService = app.ctx.PasswordService

        tokenCtx = app.ctx.tokenCtx
        Token = tokenCtx["Token"]
        tokenType = tokenCtx["TokenType"]
        tokenService = tokenCtx["TokenService"]

        auth_data = request.json
        pprint.pp(auth_data)

        if not auth_data:
            return sanjson(status=400, body={
                "info": "Invalid credentials"
            })

        if 'email' not in auth_data:
            return sanjson(status=400, body={
                "info": "Missing required fields"
            })
        
        if 'password' not in auth_data:
            return sanjson(status=400, body={
                "info": "Missing required field - Password"
            })
                
        if auth_data['email'] == None:
            return sanjson(status=400, body={
                "info": "Required fields cannot be empty"
            })
        if auth_data['password'] == None:
            return sanjson(status=400, body={
                "info": "Required fields cannot be empty"
            })
            
        # {"email": email, "password": password}:

        # pprint.pp(accountService.accounts)
        
        account = await accountService.fetch_user(pool, email=auth_data['email'])
        if not account:
            return sanjson(status=404, body={
                "info": "Invalid credentials"
            })
        # pprint.pp(account)        
        passCheck = passwordService.pwd_context.verify(auth_data['password'], account['password'])

        if not passCheck:
            return sanjson(status=400, body={"info": "Invalid credentials"})

        newToken = Token(
            account_id = account['account_id'],
            valid=True,
            token_type = tokenType.AUTH
        )
        gen_token = await tokenService.generate_token(pool, newToken, pvkey)
        newToken.signature = gen_token.split('.')[-1]
        await tokenService.store_token(pool, newToken)

        account["account_id"] = account["account_id"].hex
        account["join_date"] = account["join_date"].isoformat()
        pprint.pp(f"Admin data type: {type(account['admin'])}")

        response = sanjson(status=200, body={
            'info': 'Successfully logged in',
            'authenticated': True,
            'data': account,
            'token': gen_token
        })
        # response.add_cookie(
        #     'auth_token',
        #     gen_token,
        #     max_age = newToken.expiry.timestamp(),
        #     httponly = True
        # )

        return response

    except Exception as e:
        pprint.pp(e)
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
        email_verification = app.ctx.tasks['email_verification']

        adminCtx = app.ctx.adminCtx
        Admin = adminCtx["Admin"]
        adminRole = adminCtx["AdminRole"]
        adminService = adminCtx["AdminService"]

        passwordService = app.ctx.PasswordService

        tokenCtx = app.ctx.tokenCtx
        Token = tokenCtx["Token"]
        tokenType = tokenCtx["TokenType"]
        tokenService = tokenCtx["TokenService"]

        form_data = request.json
        pprint.pp(form_data)

        if not form_data:
            return sanjson(status=400, body={'info': 'Bad request'})

        if not form_data['email']:
            return sanjson(status=400, body={'info': 'Misssing required field: email'})

        if not form_data['password']:
            return sanjson(status=400, body={'info': 'Misssing required field: password'})

        if not form_data['password2']:
            return sanjson(status=400, body={'info': 'Misssing required field: password2'})

        if not form_data['phone']:
            return sanjson(status=400, body={'info': 'Misssing required field: phone'})

        if not form_data['firstname']:
            return sanjson(status=400, body={'info': 'Misssing required field: firstname'})
        if not form_data['lastname']:
            return sanjson(status=400, body={'info': 'Misssing required field: lastname'})

        if form_data['password'] != form_data['password2']:
            return sanjson(status=400, body={'info': 'Passwords do not match'})

        user = await accountService.fetch_user(pool=pool, email=form_data['email'])
        if user:
            return sanjson(status=409, body={'info': 'This email is already registered'})
        
        new_account = Account(
            email=form_data['email'], 
            phone_number=PhoneNumber(form_data['phone']),
            password=passwordService.pwd_context.hash(form_data['password']),
            firstname=form_data['firstname'],
            lastname=form_data['lastname'],
            othername=form_data['othername'],
            is_admin=False
        )
        account_created = await accountService.create_account(pool, new_account)
                        
        if not account_created:
            return sanjson(status=500, body={'info': 'An error occurred during account creation.'})

        # Create verification link
        verification_link = await app.ctx.EmailVerificationLink.create_link(accountid=new_account.account_id, email=new_account.email)
        # pprint.pp(app.config)
        
        # Send verification email
        await asyncio.to_thread(
            email_verification,
            password=app.config.mail['PASSWORD'],
            link=verification_link,
            messageFrom=app.config.mail['NOREPLY'],
            messageTo=new_account.email
        )
        return sanjson(status=200, body={
            'info': 'Success'
            })

    except Exception as e:
        raise e


async def confirm_account(request: Request, token: str):
    """ Confirm a user's email account """
    try:
        if not token:
            return sanjson(status=400, body={
                'info': 'Bad request'
            })

        app = request.app
        pool = app.ctx.pool
        
        EmailVerificationLink = app.ctx.EmailVerificationLink
        Account = app.ctx.accountCtx['Account']
        accountService = app.ctx.accountCtx['AccountService']
        tokenCtx = app.ctx.tokenCtx 
        Token = tokenCtx['Token']
        tokenType = tokenCtx['TokenType']
        tokenService = app.ctx.tokenCtx['TokenService']
        
        verifyAccount = await EmailVerificationLink.verify_token(token)
        pprint.pp(verifyAccount)

        if not verifyAccount:
            return sanjson(status400, body={
                'info': 'Bad request'
                })

        account = await accountService.fetch_user(pool=pool, email=verifyAccount['email'])        
        newToken = Token(
            account_id = account['account_id'],
            valid = True,
            token_type = tokenType.AUTH
        )
        gen_token = await tokenService.generate_token(pool, newToken, pvkey)
        newToken.signature = gen_token.split('.')[-1]
                        
        account_dict = dict(new_account)
        account_dict.pop('password')
        await tokenService.store_token(pool, newToken)

        account_dict["account_id"] = account_dict["account_id"].hex
        account_dict['join_date'] = account_dict['join_date'].isoformat()

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


