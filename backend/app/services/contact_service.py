from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.schemas.contact import ContactCreate
from fastapi import HTTPException



def create_contact(
    db: Session,
    contact_data: ContactCreate
):
    
    existing_contact = db.query(Contact).filter(
        Contact.email == contact_data.email
    ).first()

    if existing_contact:
        raise HTTPException(
            status_code=400,
            detail="Contact already exists"
        )

    contact = Contact(
        first_name=contact_data.first_name,
        last_name=contact_data.last_name,
        email=contact_data.email,
        phone=contact_data.phone,
        organization=contact_data.organization
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact

def get_contacts(
    db: Session
):
    return db.query(Contact).all()