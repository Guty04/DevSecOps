from typing import Annotated

import logfire
from fastapi import APIRouter, Depends, HTTPException, Security, status

from src.database.models import User as UserDB
from src.enums import Message, Permission
from src.errors import UserAlreadyExistError
from src.schemas import User, UserCreate
from src.services import UserService
from src.utils import get_translate

from .dependencies import get_current_user, get_language, get_user_service

router: APIRouter = APIRouter(prefix="/user", tags=["User"])


@router.get("/")
async def route_get_users(
    service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[UserDB, Security(get_current_user, scopes=[Permission.READ_USERS])],
) -> list[User]:
    logfire.info("", user_id=current_user.id)  # TODO: Definir un estandar para los logs

    return await service.get_all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def router_post_user(
    user_create: UserCreate,
    language: Annotated[str, Depends(get_language)],
    service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    try:
        return await service.create_user(user_create=user_create)

    except UserAlreadyExistError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=get_translate(language=language, message=Message.USER_ALREADY_EXIST),
        ) from e
