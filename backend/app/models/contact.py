from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base
from sqlalchemy.orm import relationship


class Contact(Base):

    __tablename__ = "contacts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    first_name = Column(
        String,
        nullable=False
    )

    last_name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        nullable=True,
        unique=True
    )

    phone = Column(
        String,
        nullable=True,
        unique=True
    )

    organization = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    campaigns = relationship(
        "Campaign",
        secondary="campaign_contacts",
        back_populates="contacts"
    )