from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Users, Role
from src.schemas import UserResponse, UserModel, UserEmailModel
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.services.roles import RoleAccess


router = APIRouter(prefix="/users", tags=["users"])

allowed_operation_get = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_create = RoleAccess([Role.admin, Role.moderator])
allowed_operation_update = RoleAccess([Role.admin, Role.moderator])
allowed_operation_remove = RoleAccess([Role.admin])


@router.get(
    "/",
    response_model=List[UserResponse],
    dependencies=[Depends(allowed_operation_get)],
)
async def get_users(
    db: Session = Depends(get_db),
    curent_user: Users = Depends(auth_service.get_current_user),
):
    users = await repository_users.get_users(db)
    return users


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(allowed_operation_get)],
)
async def get_user(
    user_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    curent_user: Users = Depends(auth_service.get_current_user),
):
    user = await repository_users.get_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(allowed_operation_create)],
)
async def create_user(
    body: UserModel,
    db: Session = Depends(get_db),
    curent_user: Users = Depends(auth_service.get_current_user),
):
    user = await repository_users.create_user(body, db)
    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(allowed_operation_update)],
    description="Only moderator and admin",
)
async def update_user(
    body: UserModel,
    user_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    curent_user: Users = Depends(auth_service.get_current_user),
):
    user = await repository_users.update_user(body, user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(allowed_operation_update)],
    description="Only moderator and admin",
)
async def update_user_email(
    body: UserEmailModel,
    user_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    curent_user: Users = Depends(auth_service.get_current_user),
):
    user = await repository_users.update_user_email(body, user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(allowed_operation_remove)],
    description="Only admin",
)
async def remove_user(
    user_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    curent_user: Users = Depends(auth_service.get_current_user),
):
    user = await repository_users.remove_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.get(
    "/search/",
    response_model=List[UserResponse],
    dependencies=[Depends(allowed_operation_get)],
)
async def search_user(
    q: str = Query(description="Search by name, last name or email"),
    skip: int = 0,
    limit: int = Query(
        default=10,
        le=100,
        ge=10,
    ),
    db: Session = Depends(get_db),
    curent_user: Users = Depends(auth_service.get_current_user),
):
    users = await repository_users.search_user(db, q, skip, limit)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return users


@router.get(
    "/birthdays/",
    response_model=List[UserResponse],
    dependencies=[Depends(allowed_operation_get)],
)
async def birthday_users(
    days: int = Query(default=7, description="Enter the number of days"),
    skip: int = 0,
    limit: int = Query(
        default=10,
        le=100,
        ge=10,
    ),
    db: Session = Depends(get_db),
    curent_user: Users = Depends(auth_service.get_current_user),
):
    birthday_users = await repository_users.birthdays_per_week(db, days, skip, limit)
    if birthday_users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return birthday_users