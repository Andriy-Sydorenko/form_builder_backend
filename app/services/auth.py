import datetime
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AuthService:
    @staticmethod
    def generate_jwt_token(user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.datetime.now(datetime.UTC)
            + datetime.timedelta(minutes=settings.jwt_access_token_expire_minutes),
        }
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_encrypt_algorithm)

    @staticmethod
    def decode_jwt(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_encrypt_algorithm])
            user_id: str = payload["user_id"]
        except (KeyError, ValueError) as err:
            raise jwt.InvalidTokenError from err
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired") from None
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token") from None

        return user_id
