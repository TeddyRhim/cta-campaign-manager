from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.campaign import Campaign
from app.models.contact import Contact
from app.models.imports import Import


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {
        "campaigns_count": db.query(Campaign).count(),
        "contacts_count": db.query(Contact).count(),
        "imports_count": db.query(Import).count()
    }