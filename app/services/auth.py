from datetime import datetime, timedelta, timezone
from fastapi import Response
from passlib.context import CryptContext
from app.config import settings
import jwt

from app.error import ServiceException


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(
        self, plain_password, hashed_password
    ) -> bool:
        return self.pwd_context.verify(
            plain_password, hashed_password
        )

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=settings.JWT_ALGORITHM,
            )
        except jwt.exceptions.DecodeError:
            raise ServiceException("Неверный токен доступа")

    def logout_session(self, token, response: Response):
        if token:
            response.delete_cookie("access_token")
        return {"status": "OK"}
