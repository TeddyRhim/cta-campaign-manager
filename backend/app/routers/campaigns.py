from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.campaign import (CampaignCreate, CampaignResponse, CampaignUpdate)
from app.models.user import User
from app.models.contact import Contact
from app.core.dependencies import (get_current_user, get_db)
from app.services.campaign_service import (create_campaign, get_campaigns_service, get_campaign_by_id, update_campaign_service, delete_campaign_service)
from app.services.campaign_contact_service import add_contact_to_campaign
from app.models.enums import UserRole


router = APIRouter(
    prefix="/campaigns",
    tags=["Campaigns"]
)

@router.post(
    "",
    response_model=CampaignResponse
)
def create(
    campaign_data: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return create_campaign(
        db,
        campaign_data,
        current_user
    )


@router.get(
    "/",
    response_model=list[CampaignResponse]
)
def get_campaigns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_campaigns_service(db, current_user)


@router.get(
    "/{campaign_id}",
    response_model=CampaignResponse
)
def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    campaign = get_campaign_by_id(
        db,
        campaign_id,
    )

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
            detail="You don't have permission to access this campaign"
        )

    return campaign

@router.put(
    "/{campaign_id}",
    response_model=CampaignResponse
)
def update_campaign(
    campaign_id: int,
    campaign_data: CampaignUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    campaign = get_campaign_by_id(
        db,
        campaign_id
    )

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


    return update_campaign_service(
        db,
        campaign,
        campaign_data.title,
        campaign_data.description
    )

@router.delete("/{campaign_id}")
def delete_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    campaign = get_campaign_by_id(
        db,
        campaign_id
    )

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


    delete_campaign_service(
        db,
        campaign
    )


    return {
        "message": "Campaign deleted successfully"
    }

@router.post(
    "/{campaign_id}/contacts/{contact_id}",
    response_model=CampaignResponse
)
def link_contact_to_campaign(
    campaign_id: int,
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    campaign = get_campaign_by_id(
        db,
        campaign_id,
    )

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


    contact = db.query(Contact).filter(
        Contact.id == contact_id
    ).first()


    if not contact:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )


    return add_contact_to_campaign(
        db,
        campaign,
        contact
    )