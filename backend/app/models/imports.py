from datetime import datetime

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Import(Base):
    __tablename__ = "imports"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    filename: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="PENDING"
    )

    success_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    error_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )