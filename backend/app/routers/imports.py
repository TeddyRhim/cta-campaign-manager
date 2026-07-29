from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.dependencies import (get_db, get_current_user)
from app.models.user import User
from app.services.imports_service import (create_import, get_imports, get_import)


router = APIRouter(
    prefix="/imports",
    tags=["Imports"]
)


@router.post("/")
def upload_import(
    campaign_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_import(
        db=db,
        file_name=file.filename,
        campaign_id=campaign_id,
        file=file,
        current_user=current_user
    )

@router.get("/")
def list_imports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_imports(
        db=db,
        current_user=current_user
    )

@router.get("/{import_id}")
def get_import_by_id(
    import_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_import(
        db=db,
        import_id=import_id,
        current_user=current_user
    )