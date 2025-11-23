from itsdangerous.url_safe import URLSafeTimedSerializer
from datetime import datetime, timezone
from enum import Enum
from sanic import Sanic


class MagicEnum(Enum):
    VERICATION = "verification"
    RESET = "reset"


class SecureMagicLink:
    def __init__(self, app: Sanic, secret_key: str, link_type: str):
        self.app = app
        self.serializer = URLSafeTimedSerializer(secret_key, salt=link_type)
        self.link_type = link_type


    async def create_link(self, userid: str, email: str, expires_min: int = 10) -> str:
        payload = {
            "user_id": userid.hex,
            "email": email,
            "iat": int(datetime.now(timezone.utc).timestamp())
        }
        token = self.serializer.dumps(payload)

        match self.app.config.app['ENV']:
            case 'dev':
                match self.link_type:
                    case "verify":
                        return f"https://{self.app.config.app['HOST']}:{self.app.config.app['PORT']}/account/verify?token={token}"
                    case "reset":
                        return f"https://{self.app.config.app['HOST']}:{self.app.config.app['PORT']}/account/reset/link?token={token}"

            case 'prod':
                match self.link_type:
                    case "verify":
                        return f"https://{self.app.config.app['DOMAIN']}/account/verify?token={token}"
                    case "reset":
                        return f"https://{self.app.config.app['DOMAIN']}/accoint/reset?token={token}"


    async def verify_token(self, token: str, max_age: int = 600) -> dict | None:
        try:
            return self.serializer.loads(token, max_age=max_age)
        except Exception as e:
            pprint(e)
            # return None
            raise e
