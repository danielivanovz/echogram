from fastapi import APIRouter, Depends, HTTPException, status

from api.db.client import create_supabase_client
from api.db.schemas import Attachment
from api.security import get_current_user

attachment_router = APIRouter(
    prefix="/attachments",
    tags=["attachments"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_user)],
)


@attachment_router.get("/{attachment_id}")
async def get_attachment(attachment_id: str):
    client = create_supabase_client()
    attachment = (
        client.table("attachments")
        .select("*")
        .eq("id", attachment_id)
        .single()
        .execute()
    )

    if attachment.data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attachment with id <{attachment_id}> not found.",
        )

    return Attachment(
        attachment_id=attachment.data.attachment_id,
        email_id=attachment.data.email_id,
        url=attachment.data.url,
        file_name=attachment.data.file_name,
    )
