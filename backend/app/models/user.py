from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum

from app.db.database import Base

from app.models.enums import UserRole


class User(Base):

    __tablename__ = "users"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )


    password_hash = Column(
        String,
        nullable=False
    )


    first_name = Column(
        String,
        nullable=True
    )


    last_name = Column(
        String,
        nullable=True
    )


    role = Column(
    Enum(UserRole),
    nullable=False,
    default=UserRole.OPERATOR
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )