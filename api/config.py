from functools import lru_cache
from pydantic import BaseModel, Field

from pydantic_settings import BaseSettings, SettingsConfigDict


class CollectorSettings(BaseModel):
    retry_interval: int = 5
    max_retry_interval: int = 360


class Settings(BaseSettings):
    supabase_url: str = Field(validation_alias="SUPABASE_URL")
    supabase_key: str = Field(validation_alias="SUPABASE_KEY")
    supabase_uri: str = Field(validation_alias="SUPABASE_URI")

    imap_host: str = Field(validation_alias="EMAIL_HOST")
    imap_port: int = Field(validation_alias="EMAIL_PORT")
    imap_username: str = Field(validation_alias="EMAIL_USERNAME")
    imap_password: str = Field(validation_alias="EMAIL_PASSWORD")

    jwt_secret: str = Field(validation_alias="JWT_SECRET")

    collector: CollectorSettings = CollectorSettings()

    model_config = SettingsConfigDict(extra="allow")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
