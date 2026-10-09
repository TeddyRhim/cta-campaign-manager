from sqlalchemy.orm import Session

from app.models.campaign import Campaign
from app.models.user import User
from fastapi import HTTPException

from app.schemas.campaign import CampaignCreate, CampaignUpdate
from app.models.enums import CampaignStatus, UserRole


def create_campaign(
    db: Session,
    campaign_data: CampaignCreate,
    current_user: User
):

    campaign = Campaign(
        title=campaign_data.title,
        description=campaign_data.description,
        status=CampaignStatus.DRAFT,
        created_by=current_user.id
    )

    db.add(campaign)
    db.commit()
    db.refresh(campaign)

    return campaign

def get_campaigns_service(
    db: Session,
    current_user: User
):

    if current_user.role == UserRole.ADMIN:
        return db.query(Campaign).all()


    return db.query(Campaign).filter(
        Campaign.created_by == current_user.id
    ).all()


def get_campaign_by_id(
    db: Session,
    campaign_id: int,
):

    query = db.query(Campaign).filter(
        Campaign.id == campaign_id
    )

    return query.first()


def update_campaign_service(
    db: Session,
    campaign: Campaign,
    campaign_data: CampaignUpdate
):

    changes = campaign_data.model_dump(exclude_unset=True)

    if "title" in changes and not changes["title"]:
        raise HTTPException(
            status_code=422,
            detail="Title cannot be empty"
        )

    if changes.get("status") is None:
        changes.pop("status", None)

    for field, value in changes.items():
        setattr(campaign, field, value)

    db.commit()
    db.refresh(campaign)

    return campaign

def delete_campaign_service(
    db: Session,
    campaign: Campaign
):

    db.delete(campaign)
    db.commit()