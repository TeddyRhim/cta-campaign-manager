from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.db.database import SessionLocal

from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user
from app.schemas.user import UserLogin
from app.services.auth_service import authenticate_user
from app.core.dependencies import get_current_user




router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)



def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


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

    token = authenticate_user(
        db,
        user_data.email,
        user_data.password
    )

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