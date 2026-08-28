from datetime import datetime, timedelta, timezone
import jwt
from app.config import settings


class JWTService:

    @classmethod
    def create_access_token(
        cls,
        user_id: int
    ) -> str:

        now = datetime.now(timezone.utc)

        expires_at = (
            now
            + timedelta(
                minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )

        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": expires_at,
            "type": "access",
        }

        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )


    @classmethod
    def decode_access_token(
        cls,
        token: str
    ) -> dict:

        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )