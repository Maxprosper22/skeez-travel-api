from sanic import Sanic

async def setupECDSA_Keys(app: Sanic) -> None:
	""" Setup ECDAS Keys """

	with open("bpp/components/auth/certificates/private_key.pem", "r") as pvfile:
		app.ctx.pvkey = pvfile.read()
		pvfile.close()
		
	with open("bpp/components/auth/certificates/public_key.pem", "r") as pbfile:
		app.ctx.pbkey = pbfile.read()
		pbfile.close()
