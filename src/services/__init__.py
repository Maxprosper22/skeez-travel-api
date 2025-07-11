from sanic import Sanic

from .keys import setupECDSAKeys
from .password import PasswordService

from .account import AccountService
from src.models.account import Account

from .trip import TripService
from src.models.trip import Trip, TripStatus

from .token import TokenService
from src.models.token import Token, TokenType

from .admin import AdminService
from src.models.admin import Admin, AdminRole

from.ticket import TicketService
from src.models.ticket import Ticket

async def register_services(app: Sanic) -> None:
    """ Register services """
    
    # Admin context varuables
    app.ctx.adminCtx = {
        "Admin": Admin,
        "AdminRole": AdminRole,
        "AdminService": AdminService
    }
    # Create new table table if it doesn't exist
    await app.ctx.adminCtx["AdminService"].create_table(pool=app.ctx.pool)

    # app.ctx.AccountModel = Account
    app.ctx.accountCtx = {
        "Account": Account,
        "AccountService": AccountService()
    }

    # Create new accounts table if it doesn't exist
    await app.ctx.accountCtx["AccountService"].create_table(pool=app.ctx.pool)
    
    # Retrieve and populate Accounts array of the AccountController
    await app.ctx.accountCtx["AccountService"].populate_accounts(app.ctx.pool)

    app.ctx.tripCtx = {
        'TripService': TripService,
        'TripStatus': TripStatus,
        'Trip': Trip
    }

    # Create trips table
    await app.ctx.tripCtx["TripService"].create_trip_table(app.ctx.pool)
    await app.ctx.tripCtx["TripService"].create_ticket_table(app.ctx.pool)

    # Populate trip array
    await app.ctx.tripCtx["TripService"].populate_trips(app.ctx.pool)

    await setupECDSAKeys(app)  # Set up encryption keys

    app.ctx.PasswordService = PasswordService

    app.ctx.tokenCtx = {
        "Token": Token,
        "TokenType": TokenType,
        "TokenService": TokenService
    }

    await app.ctx.tokenCtx["TokenService"].create_table(app.ctx.pool)

    app.ctx.ticketCtx = {
        "Ticket": Ticket,
        "TicketService": TicketService
    }

    await app.ctx.ticketCtx["TicketService"].create_table(app.ctx.pool)
