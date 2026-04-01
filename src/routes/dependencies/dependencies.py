from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import database
from src.database.models import User
from src.enums import Language, Message
from src.errors import AuthenticationError, AuthorizationError
from src.repositories import UserRepository
from src.services import AuthService, UserService
from src.utils import get_translate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_auth_service(
    session: AsyncSession = Depends(dependency=database.get_async_session),
) -> AuthService:
    return AuthService(_repository=UserRepository(_session=session))


def get_user_service(session: AsyncSession = Depends(dependency=database.get_async_session)) -> UserService:
    return UserService(_repository=UserRepository(session))


def get_language(request: Request) -> Language:
    language: str = request.get("Accept-Language", "en")

    return Language(language.split(",")[0])


async def get_current_user(
    security: SecurityScopes,
    auth_service: AuthService = Depends(dependency=get_auth_service),
    language: Language = Depends(get_language),
    access_token: str = Depends(dependency=oauth2_scheme),
) -> User:
    try:
        return await auth_service.get_current_user(
            access_token=access_token,
            required_scopes=set(security.scopes),
        )

    except AuthenticationError as auth_error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=get_translate(language=language, message=Message.INVALID_CREDENTIALS),
            headers={"WWW-Authenticate": "Bearer"},
        ) from auth_error

    except AuthorizationError as permissions_error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=get_translate(language=language, message=Message.INSUFFICIENT_PERMISSION),
        ) from permissions_error
