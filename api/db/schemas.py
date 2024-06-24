from datetime import datetime
import uuid
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    user_id: str
    email: EmailStr
    created_on: str


class UserCreate(BaseModel):
    email: EmailStr


class MagicLink(BaseModel):
    token: str
    email: str


class Email(BaseModel):
    email_id: str
    user_id: str
    subject: str
    body: str
    received_on: str


class EmailCreate(BaseModel):
    user_id: str
    subject: str
    body: str
    received_on: str

    @classmethod
    def from_msg(cls, msg):
        return cls(
            user_id=msg.from_,  # This is a placeholder, the actual value should be the user_id of the user who sent the email
            subject=msg.subject,
            body=msg.text,
            received_on=datetime.strftime(msg.date, "%Y-%m-%d %H:%M:%S"),
        )


class Attachment(BaseModel):
    attachment_id: str
    email_id: str
    file_name: str
    url: str


class AttachmentCreate(BaseModel):
    email_id: str
    file_name: str
    blob: bytes
