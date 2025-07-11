# Looking to send emails in production? Check out our Email API/SMTP product!
import smtplib

async def send_mail():
    """ Send email """

    sender = "Private Person <from@example.com>"
    receiver = "A Test User <to@example.com>"

    message = f"""\
        Subject: Hi Mailtrap
        To: {receiver}
        From: {sender}

        This is a test e-mail message.
    """

    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.starttls()
        server.login("23645fcee67e83", "05de817e223a0d")
        server.sendmail(sender, receiver, message)
