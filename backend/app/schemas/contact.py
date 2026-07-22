from datetime import datetime
from pydantic import BaseModel, EmailStr, model_validator, ConfigDict


class ContactBase(BaseModel):
    first_name: str | None = None
    last_name: str
    email: EmailStr | None = None
    phone: str | None = None
    organization: str | None = None

class ContactCreate(ContactBase):

    @model_validator(mode="after")
    def check_contact_method(self):

        if not self.email and not self.phone:
            raise ValueError(
                "A contact must have an email or a phone number"
            )

        return self
    
class ContactResponse(ContactBase):

    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
