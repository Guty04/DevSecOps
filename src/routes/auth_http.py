from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_limiter.depends import RateLimiter
from jwt import InvalidTokenError
from pyrate_limiter import Duration, Limiter, Rate

from src.configurations import configuration
from src.enums import Environment, Message
from src.errors import AuthenticationError, AuthorizationError, UserNotFoundError
from src.schemas import Token, Tokens
from src.services import AuthService
from src.utils import get_translate

from .dependencies import get_auth_service, get_language

router: APIRouter = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", dependencies=[Depends(RateLimiter(Limiter(Rate(3, Duration.SECOND * 5))))])
async def route_login(
    response: Response,
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(dependency=get_auth_service)],
    language: Annotated[str, Depends(dependency=get_language)],
) -> Token:
    try:
        login_result: Tokens = await auth_service.login(email=credentials.username, password=credentials.password)

    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(get_translate(language=language, message=Message.INVALID_CREDENTIALS)),
        ) from e

    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(get_translate(language=language, message=Message.USER_NOT_FOUND)),
        ) from e

    response.set_cookie(
        key="refresh_token",
        value=login_result.refresh_token,
        domain=configuration.DOMAIN,
        httponly=True,
        secure=configuration.ENVIRONMENT in [Environment.PRODUCTION, Environment.STAGING],
        samesite="lax",
        max_age=60 * 60 * 24,
    )

    return login_result.access_token


@router.post(path="/refresh_token")
async def route_refresh_token(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    language: Annotated[str, Depends(get_language)],
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> Token:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is missing.",
        )

    try:
        return await auth_service.refresh_token(refresh_token)

    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token.",
        ) from e

    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=get_translate(language=language, message=Message.INVALID_CREDENTIALS),
        ) from e

    except AuthorizationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=get_translate(language=language, message=Message.INSUFFICIENT_PERMISSION),
        ) from e


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def route_logout(response: Response) -> None:
    response.delete_cookie(
        key="refresh_token",
        domain=configuration.DOMAIN,
        httponly=True,
        secure=configuration.ENVIRONMENT in [Environment.PRODUCTION, Environment.STAGING],
        samesite="lax",
    )
