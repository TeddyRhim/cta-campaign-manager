from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.core.pagination import PageParams, page_params, paginate
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.contact import ContactCreate, ContactResponse
from app.schemas.pagination import Page
from app.services.contact_service import create_contact, get_contacts

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
    response_model=Page[ContactResponse]
)
def get_all(
    params: PageParams = Depends(page_params),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only admins can access contacts"
        )

    return paginate(get_contacts(db, params.search), params)