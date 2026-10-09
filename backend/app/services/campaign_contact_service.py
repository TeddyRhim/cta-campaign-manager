from sqlalchemy.orm import Session

from app.models.campaign import Campaign
from app.models.contact import Contact


def add_contact_to_campaign(
    db: Session,
    campaign: Campaign,
    contact: Contact
):
    if contact not in campaign.contacts:
        campaign.contacts.append(contact)

    db.commit()
    db.refresh(campaign)

    return campaign