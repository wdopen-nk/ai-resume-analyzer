from fastapi import APIRouter, HTTPException

from app.schemas.auth import RegisterRequest
from app.services.auth_service import AuthService
from app.services.database_service import DatabaseService


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