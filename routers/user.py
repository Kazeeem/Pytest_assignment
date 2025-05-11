# built-in libraries
from uuid import UUID
# installed libraries
from fastapi import APIRouter, HTTPException
# code libraries/folder
from database import users
from schemas.user import Response, UserCreate, UserUpdate, ChangePassword, UserLogin
from services.user import user_service


user_router = APIRouter()


@user_router.get("")
def get_users():
    return users


@user_router.get("/details/{id}")
def get_user_by_id(id: str):
    user = user_service.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.post("/create")
def create_user(user_in: UserCreate):
    user = user_service.create_user(user_in)
    return Response(message="User created successfully", data=user)


@user_router.put("/update/{id}")
def update_user(id: UUID, user_in: UserUpdate):
    user = user_service.update_user(id, user_in)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with id: {id} not found"
        )
    return Response(message="User updated successfully", data=user)


@user_router.delete("/delete/{id}")
def delete_user(id: UUID):
    is_deleted = user_service.delete_user(id)
    if not is_deleted:
        raise HTTPException(
            status_code=404,
            detail=f"User with id: {id} not found"
        )
    return Response(message="User deleted successfully")


@user_router.post("/change-password/{id}")
def change_password(id: UUID, password: ChangePassword):
    password_changed = user_service.change_password(id, password)

    if not password_changed:
        raise HTTPException(
            status_code=422,
            detail="Unprocessable entity"
        )
    return Response(message="Password changed successfully")

@user_router.post("/login")
def login(user_in: UserLogin):
    login_successful = user_service.login(user_in)

    if not login_successful:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized - Invalid login credentials"
        )

    return Response(message="Login successful", data=login_successful)