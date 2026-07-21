from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.enums import CampaignStatus


class CampaignBase(BaseModel):
    title: str
    description: str | None = None


class CampaignCreate(CampaignBase):
    pass


class CampaignResponse(CampaignBase):
    id: int
    status: CampaignStatus
    created_by: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class CampaignUpdate(BaseModel):

    title: str | None = None
    description: str | None = None