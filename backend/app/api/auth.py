from fastapi import APIRouter, HTTPException

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse
)

from app.services.auth_service import AuthService
from app.services.database_service import DatabaseService
from app.services.jwt_service import JWTService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(request: RegisterRequest):

    existing_user = DatabaseService.get_user_by_email(
        request.email
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists"
        )

    password_hash = AuthService.hash_password(
        request.password
    )

    user = DatabaseService.create_user(
        email=request.email,
        password_hash=password_hash
    )

    return {
        "id": user.id,
        "email": user.email,
        "message": "User registered successfully."
    }


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(request: LoginRequest):

    user = DatabaseService.get_user_by_email(
        request.email
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    valid_password = AuthService.verify_password(
        request.password,
        user.password_hash
    )

    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )


    access_token = JWTService.create_access_token(
        user.id
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }