from sqlalchemy.orm import Session

from app.models.campaign import Campaign
from app.models.user import User
from app.schemas.campaign import CampaignCreate
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
    title: str,
    description: str | None
):

    campaign.title = title
    campaign.description = description

    db.commit()
    db.refresh(campaign)

    return campaign

def delete_campaign_service(
    db: Session,
    campaign: Campaign
):

    db.delete(campaign)
    db.commit()