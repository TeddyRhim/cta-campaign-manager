from sqlalchemy.orm import Session
from fastapi import UploadFile


from app.models.imports import Import
from app.models.user import User, UserRole
from app.models.contact import Contact
from app.models.campaign import Campaign
from app.models.contact_campaign import CampaignContact
from fastapi import HTTPException
from app.services.importers.csv_importers import read_csv
from datetime import datetime, timezone


def create_import(
    db: Session,
    file_name: str,
    campaign_id: int,
    file: UploadFile,
    current_user: User
):

    required_fields = [
        "first_name",
        "last_name",
        "email",
        "phone"
    ]

    rows = read_csv(file)
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )

    new_import = Import(
        filename=file_name,
        campaign_id=campaign_id,
        created_by_id=current_user.id,
        source_type="MANUAL",
        status="PENDING"
    )
    db.add(new_import)


    success_count = 0
    error_count = 0
    for row in rows:

        if any(not row.get(field) for field in required_fields):
            error_count += 1
            continue

        if "@" not in row["email"]:
            error_count += 1
            continue

        existing_contact = db.query(Contact).filter(
            (Contact.email == row["email"]) |
            (Contact.phone == row["phone"])
        ).first()

        if existing_contact:
            contact = existing_contact

        else :
            contact = Contact(
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
                phone=row["phone"],
                organization=row["organization"]
            )

            db.add(contact)
            db.flush()

        existing_association = db.query(CampaignContact).filter(
            CampaignContact.campaign_id == campaign_id,
            CampaignContact.contact_id == contact.id
        ).first()

        if not existing_association:
            association = CampaignContact(
                campaign_id=campaign_id,
                contact_id=contact.id
            )
        
            db.add(association)

        success_count += 1

    new_import.success_count = success_count
    new_import.error_count = error_count
    if error_count == 0:
        new_import.status = "SUCCESS"
    elif success_count > 0:
        new_import.status = "PARTIAL"
    else:
        new_import.status = "FAILED"
    new_import.processed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(new_import)

    return new_import

def get_imports(
    db: Session,
    current_user: User
):
    if current_user.role == UserRole.ADMIN:
        return db.query(Import).all()

    return db.query(Import).filter(
        Import.created_by_id == current_user.id
    ).all()


def get_import(
    db: Session,
    import_id: int,
    current_user: User
):
    import_ = db.query(Import).filter(
        Import.id == import_id
    ).first()

    if not import_:
        raise HTTPException(
            status_code=404,
            detail="Import not found"
        )

    if (
        current_user.role != UserRole.ADMIN
        and import_.created_by_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )

    return import_