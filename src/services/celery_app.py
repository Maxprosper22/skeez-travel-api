from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sanic import Sanic
import smtplib

from celery import Celery


app = Celery('skrid', broker='redis://localhost:6379/1')

#async def celery_app():
#    """ Setup celery app """


@app.task
def email_verification(password: str, link: str, messageFrom: str, messageTo: str):
    """ Function for sending email verification links """
    try:
        message = EmailMessage()
        message['FROM'] = messageFrom
        message['TO'] = messageTo
        message['SUBJECT'] = "Account Verification"
        message.set_content(f"{link}")

        with smtplib.SMTP("smtp.zoho.com", 587) as server:
            print(server.__dir__())
            server.starttls()
            server.login(messageFrom, password)
            server.send_message(message)

    except Exception as e:
        raise e


@app.task
def email_reset_link(password: str, link: str, messageFrom: str, messageTo: str):
    """ Function for Sending password reset links """
    try:
        message = EmailMessage()
        message['FROM'] = messageFrom
        message['TO'] = messageTo
        message['SUBJECT'] = "Password Reset"
        message.set_content(f"{link}")

        with smtplib.SMTP("smtp.zoho.com", 587) as server:
            server.starttls()
            server.login(messageFrom, password)
            server.send_message(message)

    except Exception as e:
        raise e
