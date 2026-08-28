from typing import Annotated

import jwt

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models.user import User
from app.services.database_service import DatabaseService
from app.services.jwt_service import JWTService


security = HTTPBearer(
    auto_error=False
)


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(security)
    ]
) -> User:

    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required."
        )

    token = credentials.credentials

    try:

        payload = JWTService.decode_access_token(token)

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=401,
            detail="Token has expired."
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token."
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token."
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token."
        )

    try:
        user_id = int(user_id)

    except (TypeError, ValueError):

        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token."
        )

    user = DatabaseService.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User no longer exists."
        )

    return user