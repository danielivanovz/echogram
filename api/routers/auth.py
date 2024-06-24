import dbm
import json
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
import uuid
import smtplib
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import EmailStr

from api.config import get_settings
from api.db.actions import create_user, get_user_by_email
from api.db.client import create_supabase_client
from api.db.schemas import MagicLink, UserCreate
from api.routers.models import UserAccessToken

ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = "HS256"

magic_link_route = APIRouter(
    prefix="/auth/magiclink",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


def create_access_token(data: dict) -> str:
    settings = get_settings()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        settings = get_settings()
        return jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None


def store_magic(magic_link) -> None:
    with dbm.open("magic-links-db", "c") as db:
        token_info = {
            "token": magic_link.token,
            "email": magic_link.email,
            "timestamp": datetime.now().timestamp(),
        }
        db[magic_link.token] = json.dumps(token_info)


def send_magic_link(email: str, token: str) -> None:
    settings = get_settings()

    msg = f"Click here to login: http://localhost:3000/auth/magiclink/validate/{token}"
    subject = "Magic Link Login"

    with smtplib.SMTP_SSL(settings.imap_host, 465) as server:
        server.login(settings.imap_username, settings.imap_password)
        server.sendmail("no-reply@echogram.ink", email, f"Subject: {subject}\n\n{msg}")


@magic_link_route.post(
    "/generate",
    response_model=MagicLink,
    status_code=status.HTTP_201_CREATED,
)
async def create_magic_link(
    email: EmailStr = Body(..., embed=True, alias="email", description="Email address"),
) -> MagicLink:
    client = create_supabase_client()
    user = get_user_by_email(client, email)

    if user is None:
        create_user(client, UserCreate(email=email))

    magic_link = MagicLink(token=str(uuid.uuid4()), email=email)
    store_magic(magic_link)
    send_magic_link(email, magic_link.token)

    return magic_link.model_dump()


@magic_link_route.get(
    "/validate/{token}",
    response_model=UserAccessToken,
    status_code=status.HTTP_200_OK,
)
async def verify_magic_link(token: str) -> Optional[UserAccessToken]:
    with dbm.open("magic-links-db", "c") as db:
        stored_token = db.get(token)

        if (
            stored_token
            and (datetime.now().timestamp() - json.loads(stored_token)["timestamp"])
            < 3600
        ):
            client = create_supabase_client()
            user = get_user_by_email(client, json.loads(stored_token)["email"])
            del db[token]

            if user:
                access_token = create_access_token(data={"sub": user.email})
                return {"user": user.model_dump(), "access_token": access_token}

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )
