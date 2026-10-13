from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ImportResponse(BaseModel):
    id: int
    filename: str
    status: str
    success_count: int
    error_count: int
    source_type: str
    campaign_id: int
    created_by_id: int | None
    created_at: datetime
    processed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
