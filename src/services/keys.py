from sanic import Sanic

async def setupECDSAKeys(app: Sanic) -> None:
	""" Setup ECDAS Keys """

	with open("src/certificates/private_key.pem", "r") as pvfile:
		app.ctx.pvkey = pvfile.read()
		pvfile.close()
		
	with open("src/certificates/public_key.pem", "r") as pbfile:
		app.ctx.pbkey = pbfile.read()
		pbfile.close()
