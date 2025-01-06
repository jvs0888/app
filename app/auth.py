import time
import jwt
import bcrypt
from pathlib import Path
from fastapi import Cookie
from authlib.integrations.starlette_client import OAuth

try:
    from settings.config import config
except ImportError as ie:
    exit(f'{ie} :: {Path(__file__).resolve()}')


oauth: OAuth = OAuth()
oauth.register(
    client_id=config.GOOGLE_ID,
    client_secret=config.GOOGLE_SECRET,
    **config.OAUTH['google']
)


class Auth:
    def __init__(self):
        self.key: str = config.JWT_SECRET
        self.algorithm: str = config.JWT_ALGORITHM

    def sign_jwt(self, user_id: int) -> str:
        payload: dict = {
            'id': user_id,
            'exp': time.time() + 3600
        }
        token: str = jwt.encode(payload=payload, key=self.key, algorithm=self.algorithm)
        return token

    def verify_jwt(self, token: str) -> dict:
        try:
            decoded_token: dict = jwt.decode(jwt=token, key=self.key, algorithms=[self.algorithm])
            return decoded_token
        except Exception:
            return

    def validate_token(self, access_token: str = Cookie(None)) -> dict:
        if access_token:
            return self.verify_jwt(token=access_token)

    @staticmethod
    def hash_password(password: str) -> str:
        salt: bytes = bcrypt.gensalt()
        hashed_password: bytes = bcrypt.hashpw(password.encode(), salt)
        return hashed_password.decode()

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())


auth: Auth = Auth()
