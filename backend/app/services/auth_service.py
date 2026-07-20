from sqlalchemy.orm import Session

from app.models.user import User
from app.services.user_service import get_user_by_email
from app.core.security import (
    verify_password,
    create_access_token
)


def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    token = create_access_token({
        "sub": str(user.id),
        "email": user.email
    })

    return token