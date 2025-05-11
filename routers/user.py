# built-in libraries
from uuid import UUID
# installed libraries
from fastapi import APIRouter, HTTPException
# code libraries/folder
from database import users
from schemas.user import Response, UserCreate, UserUpdate, ChangePassword
from services.user import user_service


user_router = APIRouter()


@user_router.get("")
def get_users():
    return users


@user_router.get("/{id}")
def get_user_by_id(id: str):
    user = user_service.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user