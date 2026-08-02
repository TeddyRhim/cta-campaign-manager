from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import (get_db, get_current_user)
from app.schemas.contact import (ContactCreate, ContactResponse)
from app.services.contact_service import (create_contact, get_contacts)
from fastapi import HTTPException
from app.models.user import User
from app.models.enums import UserRole



router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)


@router.post(
    "/",
    response_model=ContactResponse
)
def create(
    contact_data: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only admins can create contacts"
        )

    return create_contact(
        db,
        contact_data
    )

@router.get(
    "/",
    response_model=list[ContactResponse]
)
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only admins can access contacts"
        )

    return get_contacts(db)