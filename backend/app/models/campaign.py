from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum

from app.db.database import Base
from app.models.enums import CampaignStatus


class Campaign(Base):

    __tablename__ = "campaigns"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    title = Column(
        String,
        nullable=False
    )


    description = Column(
        String,
        nullable=True
    )


    status = Column(
        Enum(CampaignStatus),
        nullable=False,
        default=CampaignStatus.DRAFT
    )


    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )