from typing import Optional
from datetime import date

from pydantic import BaseModel, EmailStr, Field


class ContactSchema(BaseModel):
    firstname: str = Field(min_length=2, max_length=50)
    lastname: str = Field(min_length=2, max_length=50)
    e_mail: EmailStr
    birthday: date
    add_data: Optional[str] = Field(default=None, max_length=250)


class ContactUpdateSchema(ContactSchema):
    add_data: str


class ContactResponse(BaseModel):
    id: int = 1
    firstname: str
    lastname: str
    e_mail: EmailStr
    birthday: date
    add_data: str

    class Config:
            from_attributes = True

