from collections.abc import Awaitable, Callable

import logfire
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from scalar_fastapi import (
    get_scalar_api_reference,  # pyright: ignore[reportUnknownVariableType]
)
from secure import Secure

from src.configurations import configuration
from src.enums import Environment
from src.routes import auth_router, user_router

app = FastAPI(
    title=configuration.APP_NAME,
    description="API for backend",
    version="0.0.1",
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json"
    if configuration.ENVIRONMENT not in [Environment.PRODUCTION, Environment.STAGING]
    else None,
)

secure_headers: Secure = Secure().with_default_headers()

logfire.configure(
    service_name=configuration.APP_NAME,
    send_to_logfire=Environment.DEVELOPMENT == configuration.ENVIRONMENT,
    environment=configuration.ENVIRONMENT,
    token=configuration.LOGFIRE_TOKEN,
)
logfire.instrument_fastapi(app)
logfire.instrument_httpx(capture_all=True)

for router in [user_router, auth_router]:
    app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=configuration.CORS_ORIGIN,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "Accept-Language"],
)


@app.middleware("http")
async def add_secure_headers(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    response: Response = await call_next(request)

    for header, value in secure_headers.headers.items():
        response.headers[header] = value

    return response


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    return {"message": f"Welcome to {configuration.APP_NAME}"}


if configuration.ENVIRONMENT == Environment.DEVELOPMENT:
    logfire.instrument_sqlalchemy(enable_commenter=True)

    @app.get("/docs", include_in_schema=False)
    async def scalar_docs() -> HTMLResponse:
        return get_scalar_api_reference(
            openapi_url=app.openapi_url,
            title=app.title,
            hide_models=True,
        )
