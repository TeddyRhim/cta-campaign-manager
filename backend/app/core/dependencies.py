from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import decode_access_token, oauth2_scheme
from app.db.database import SessionLocal
from app.models.user import User


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


    try:
        user_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        ) from None


    user = db.query(User).filter(
        User.id == user_id
    ).first()


    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


    return user