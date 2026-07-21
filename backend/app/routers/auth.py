from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.db.database import SessionLocal

from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user
from app.schemas.user import UserLogin
from app.services.auth_service import authenticate_user
from app.core.dependencies import (get_current_user, get_db)
from app.core.permissions import require_admin
from app.core.security import create_access_token
from app.models.user import User




router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    return create_user(
        db,
        user
    )

@router.post("/login")
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db,
        user_data.email,
        user_data.password
    )

    token = create_access_token({
        "sub": str(user.id),
        "email": user.email
    })

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get(
    "/me",
    response_model=UserResponse
)
def me(
    current_user = Depends(get_current_user)
):
    return current_user


@router.get("/admin-test")
def admin_test(
    user: User = Depends(require_admin)
):

    return {
        "message": "Bienvenue admin",
        "email": user.email
    }
