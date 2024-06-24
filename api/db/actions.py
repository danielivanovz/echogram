from typing import Optional
import uuid

from pydantic import EmailStr
from api.db.schemas import (
    Attachment,
    AttachmentCreate,
    EmailCreate,
    MagicLink,
    User,
    Email,
    UserCreate,
)

from supabase import Client


def get_user_by_email(client: Client, email: str) -> Optional[User]:
    try:
        response = client.from_("users").select("*").eq("email", email).execute()
        if response.data is None:
            raise Exception(
                f"User with email '{email}' not found."
            )  # handle : not Error

        return User(**response.data[0])
    except Exception as e:
        print(f"Error: {e}")
        return None


def generate_magic_link(client: Client, email: EmailStr) -> Optional[MagicLink]:
    try:
        magic_link = (
            client.table("magic_links")
            .insert(json=MagicLink(email=email, token=str(uuid.uuid4())).model_dump())
            .execute()
        )
        
        print(f"@@ Magic Link: {magic_link}")

        return MagicLink(**magic_link.data[0])
    except Exception as e:
        raise e


def create_user(client: Client, user: UserCreate) -> Optional[User]:
    try:
        new_user = client.table("users").insert(json=user.model_dump()).execute()
        return User(**new_user.data[0])
    except Exception as e:
        if hasattr(e, "code") and e.code == "23505":
            print(f"User with email '{user.email}' already exists.")
            return None
        else:
            raise e


def create_email(client: Client, email: EmailCreate) -> Optional[Email]:
    try:
        new_email = client.table("emails").insert(json=email.model_dump()).execute()
        return Email(**new_email.data[0])
    except Exception as e:
        raise e


def create_user_bucket(client: Client, user_id: str) -> None:
    client.storage.create_bucket(user_id)


def create_attachment(
    client: Client, attachment: AttachmentCreate
) -> Optional[Attachment]:
    if attachment.email_id not in [
        bucket["name"] for bucket in client.storage.list_buckets()
    ]:
        create_user_bucket(client, attachment.email_id)

    try:
        new_attachment_file = client.storage.from_("attachments").upload(
            file=attachment.blob,
            path=attachment.email_id,
            file_options={"content-type": "image/png"},
        )

        if new_attachment_file.error is not None:
            raise Exception(new_attachment_file.error)

        file_key = client.storage.from_(attachment.email_id).get_public_url(
            attachment.file_name
        )

        if file_key.error is not None:
            raise Exception(file_key.error)

        new_attachment = (
            client.table("attachments")
            .insert(
                json={
                    "email_id": attachment.email_id,
                    "file_name": attachment.file_name,
                    "url": file_key.data["publicURL"],
                }
            )
            .execute()
        )

        return Attachment(
            attachment_id=new_attachment.data["id"],
            email_id=attachment.email_id,
            file_name=attachment.file_name,
            url=file_key,
        )
    except Exception as e:
        raise e
