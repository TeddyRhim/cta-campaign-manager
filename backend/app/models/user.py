from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.db.database import Base


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
        String,
        nullable=False,
        default="OPERATOR"
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )