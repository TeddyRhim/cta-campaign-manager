from datetime import UTC, datetime

from email_validator import EmailNotValidError, validate_email
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.campaign import Campaign
from app.models.contact import Contact
from app.models.contact_campaign import CampaignContact
from app.models.imports import Import
from app.models.user import User, UserRole
from app.services.importers.csv_importers import read_csv

REQUIRED_FIELDS = ("first_name", "last_name", "email", "phone")
LOOKUP_CHUNK = 500


def create_import(
    db: Session,
    file_name: str,
    campaign_id: int,
    file: UploadFile,
    current_user: User
):

    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if not campaign:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )

    if (
        current_user.role != UserRole.ADMIN
        and campaign.created_by != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )

    rows = read_csv(file)

    new_import = Import(
        filename=file_name,
        campaign_id=campaign_id,
        created_by_id=current_user.id,
        source_type="MANUAL",
        status="PENDING"
    )
    db.add(new_import)

    valid_rows, error_count = _clean_rows(rows)
    success_count, conflicts = _link_contacts(db, campaign_id, valid_rows)
    error_count += conflicts

    new_import.success_count = success_count
    new_import.error_count = error_count
    if error_count == 0:
        new_import.status = "SUCCESS"
    elif success_count > 0:
        new_import.status = "PARTIAL"
    else:
        new_import.status = "FAILED"
    new_import.processed_at = datetime.now(UTC)

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

def normalize_phone(phone: str) -> str:
    """Retire espaces, points, tirets et parenthèses ; garde un « + » initial."""
    digits = "".join(c for c in phone if c.isdigit())
    return ("+" + digits) if phone.strip().startswith("+") else digits


def _clean_rows(rows: list[dict]) -> tuple[list[dict], int]:
    """Lignes valides et normalisées, et nombre de lignes rejetées."""
    valid, errors = [], 0
    for raw in rows:
        row = {key: (value or "").strip() for key, value in raw.items()}
        if any(not row.get(field) for field in REQUIRED_FIELDS):
            errors += 1
            continue
        try:
            row["email"] = validate_email(
                row["email"], check_deliverability=False
            ).normalized.lower()
        except EmailNotValidError:
            errors += 1
            continue
        row["phone"] = normalize_phone(row["phone"])
        if len(row["phone"].lstrip("+")) < 6:
            errors += 1
            continue
        valid.append(row)
    return valid, errors


def _chunks(values: list[str]):
    for start in range(0, len(values), LOOKUP_CHUNK):
        yield values[start:start + LOOKUP_CHUNK]


def _link_contacts(db: Session, campaign_id: int, rows: list[dict]) -> tuple[int, int]:
    """Crée les contacts manquants et les lie à la campagne, par lots.

    Retourne (lignes importées, lignes en conflit). Une ligne dont l'e-mail et le
    téléphone désignent deux contacts différents est un conflit, pas un succès.
    """
    emails = list({row["email"] for row in rows})
    phones = list({row["phone"] for row in rows})

    by_email: dict[str, Contact] = {}
    by_phone: dict[str, Contact] = {}
    for chunk in _chunks(emails):
        for contact in db.query(Contact).filter(Contact.email.in_(chunk)):
            by_email[contact.email] = contact
            by_phone.setdefault(contact.phone, contact)
    for chunk in _chunks(phones):
        for contact in db.query(Contact).filter(Contact.phone.in_(chunk)):
            by_phone[contact.phone] = contact
            by_email.setdefault(contact.email, contact)

    matched: list[Contact] = []
    conflicts = 0
    for row in rows:
        contact_e = by_email.get(row["email"])
        contact_p = by_phone.get(row["phone"])
        if contact_e and contact_p and contact_e is not contact_p:
            conflicts += 1
            continue
        contact = contact_e or contact_p
        if contact is None:
            contact = Contact(
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
                phone=row["phone"],
                organization=row.get("organization") or None,
            )
            db.add(contact)
            by_email[contact.email] = contact
            by_phone[contact.phone] = contact
        matched.append(contact)

    db.flush()  # un seul flush : les nouveaux contacts reçoivent leur id

    linked = {
        contact_id
        for (contact_id,) in db.query(CampaignContact.contact_id).filter(
            CampaignContact.campaign_id == campaign_id
        )
    }
    for contact in matched:
        if contact.id not in linked:
            db.add(CampaignContact(campaign_id=campaign_id, contact_id=contact.id))
            linked.add(contact.id)

    return len(matched), conflicts
