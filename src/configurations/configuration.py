from typing import Any, Literal

from pydantic import Field, PostgresDsn
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict

from src.enums import Environment


class InfisicalSettings(BaseSettings):
    INFISICAL_HOST: str
    INFISICAL_CLIENT_ID: str
    INFISICAL_CLIENT_SECRET: str
    INFISICAL_PROJECT_ID: str
    ENVIRONMENT: Environment

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class InfisicalSource(PydanticBaseSettingsSource):
    def __init__(self, settings_cls: type[BaseSettings]) -> None:
        super().__init__(settings_cls)
        self._secrets: dict[str, Any] = self._fetch_secrets()

    def _fetch_secrets(self) -> dict[str, Any]:
        from infisical_sdk import InfisicalSDKClient, ListSecretsResponse  # pyright: ignore[reportMissingTypeStubs]

        credentials = InfisicalSettings()  # type: ignore

        try:
            client = InfisicalSDKClient(host=credentials.INFISICAL_HOST)

            client.auth.universal_auth.login(
                client_id=credentials.INFISICAL_CLIENT_ID,
                client_secret=credentials.INFISICAL_CLIENT_SECRET,
            )

            response: ListSecretsResponse = client.secrets.list_secrets(
                project_id=credentials.INFISICAL_PROJECT_ID,
                environment_slug=credentials.ENVIRONMENT.value,
                secret_path="/",  # noqa: S106 # nosec
            )

            return {secret.secretKey: secret.secretValue for secret in response.secrets}

        except Exception:
            return {}

    def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        value: Any | None = self._secrets.get(field_name.upper())
        return value, field_name, False

    def __call__(self) -> dict[str, Any]:
        return {
            field_name: value
            for field_name in self.settings_cls.model_fields
            if (value := self._secrets.get(field_name.upper())) is not None
        }


class Configuration(BaseSettings):
    APP_NAME: str
    ENVIRONMENT: Environment
    DATABASE_URL: PostgresDsn
    SECRET_KEY: str = Field(min_length=32)
    JWT_ALGORITHM: Literal["HS256", "HS384", "HS512"]
    ACCESS_TOKEN_EXPIRES: int
    LOGFIRE_TOKEN: str | None = None
    CORS_ORIGIN: list[str]
    DOMAIN: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            InfisicalSource(settings_cls),
        )


configuration: Configuration = Configuration()  # type:ignore
