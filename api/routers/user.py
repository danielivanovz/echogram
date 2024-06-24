from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import EmailStr

from api.db.actions import create_user
from api.db.client import create_supabase_client
from api.db.schemas import User, UserCreate
from api.security import get_current_user

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@user_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Optional[User],
    dependencies=[Depends(get_current_user)],
)
async def create_user_endpoint(
    email: Annotated[EmailStr, Query(min_length=6)],
):
    supabase = create_supabase_client()

    try:
        UserCreate(email=email)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid email address: {e}",
        )

    user = create_user(supabase, UserCreate(email=email))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email <{email}> already exists.",
        )

    return user


@user_router.get(
    "/{user_id}",
    response_model=Optional[User],
)
async def get_user_endpoint(user_id: str):
    supabase = create_supabase_client()
    user = supabase.from_("users").select("*").eq("email", user_id).single().execute()

    if user.data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email <{user_id}> not found.",
        )

    return User(**user.data)
