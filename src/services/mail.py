import os
from pydantic import BaseModel, Field
from typing import Optional

from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib

from sanic import Sanic
from src.models.account import Account

class MailConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str

async def load_mail_config(config):
    """ Load email config. Dependent on tye environment """
    env = config.get('app')["ENV"]
    match env:
        case "dev":
            # Load email config and add the password from environment
            _config = config.get("dev", {})['mail']
            _config["DEV_SMTP_PASSWORD"] = os.getenv("DEV_SMTP_PASSWORD")  # Get password from env
            if not _config["DEV_SMTP_PASSWORD"]:
                raise ValueError("DEV_SMTP_PASSWORD environment variable is not set")
            
            mailconfig = MailConfig(
                host=_config["HOST"],
                port=_config["PORT"],
                username=_config["USERNAME"],
                password=_config["DEV_SMTP_PASSWORD"]
            )
            return mailconfig

        case "prod":
            # Load database config and add the password from environment
            _config = config.get("prod", {})['mail']
            _config["PROD_SMTP_PASSWORD"] = os.getenv("PROD_SMTP_PASSWORD")  # Get password from env
            if not db_config["PROD_SMTP_PASSWORD"]:
                raise ValueError("PROD_SMTP_PASSWORD environment variable is not set")

            mailconfig = MailConfig(
                host=_config["HOST"],
                port=_config["PORT"],
                username=_config["USERNAME"],
                password=_config["DEV_SMTP_PASSWORD"]
            )
            return mailconfig
        
async def welcome_mail(app: Sanic, config: MailConfig, message: EmailMessage, account: Account):
    """ Welcome enail sent to new users """
    
    message = MIMEMultipart("alternative")
    message["From"] = "root@localhost"
    message["To"] = "somebody@example.com"
    message["Subject"] = "Welcome Message"

    message.attach(MIMEText(
        """<html>
            <body>
                <h1>Welcome! Your account was created successfully.</h1>
            </body>
        </html>
        """,
        "html",
        "utf-8"
        ))

    await aiosmtplib.send(
            message,
            hostname=config.host,
            port=config.port,
            username=config.username,
            password=config.password
            )


async def confirmation_mail(app: Sanic, config: MailConfig, message: EmailMessage, account: Account):
    """ Email sent to confirm  users' email account """

async def password_reset_mail(app: Sanic, config: MailConfig, message: EmailMessage, account: Account):
    """ Email containing a link and token sent when a password change is requested """

async def trip_alert_mail(app: Sanic, config: MailConfig, message: EmailMessage, account: Account):
    """ Email sent to alert a user about appraoching date of trips """
