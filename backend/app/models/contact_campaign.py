from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.sql import func

from app.db.database import Base


class CampaignContact(Base):
    __tablename__ = "campaign_contacts"
    __table_args__ = (
        UniqueConstraint(
            "campaign_id", "contact_id", name="uq_campaign_contacts_campaign_contact"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    campaign_id = Column(
        Integer,
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        nullable=False
    )

    contact_id = Column(
        Integer,
        ForeignKey("contacts.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )