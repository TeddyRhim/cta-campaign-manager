from fastapi import Depends, HTTPException

from app.models.user import User
from app.models.enums import UserRole

from app.core.dependencies import get_current_user


def require_admin(
    user: User = Depends(get_current_user)
):

    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user