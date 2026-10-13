from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core import login_throttle
from app.core.dependencies import get_current_user, get_db
from app.core.permissions import require_admin
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import authenticate_user
from app.services.user_service import create_user

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
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):

    return create_user(
        db,
        user
    )

@router.post("/login")
def login(
    user_data: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    # Compteurs par adresse IP et par compte : freine la recherche de mot de passe.
    client_ip = request.client.host if request.client else "inconnu"
    keys = [f"ip:{client_ip}", f"email:{user_data.email.lower()}"]
    if login_throttle.is_blocked(keys):
        raise HTTPException(
            status_code=429,
            detail="Too many failed login attempts, try again later"
        )

    user = authenticate_user(
        db,
        user_data.email,
        user_data.password
    )

    if not user:
        login_throttle.record_failure(keys)
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    login_throttle.reset(keys)

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

