"""Application configuration using Pydantic Settings."""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://supportdesk:supportdesk_dev@localhost:5432/supportdesk",
        description="Database URL",
    )

    # Redis
    redis_url: str = Field(
        default="redis://localhost:6379",
        description="Redis URL",
    )

    # Application
    debug: bool = Field(default=False, description="Debug mode")
    log_level: str = Field(default="INFO", description="Log level")
    secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        description="Secret key for JWT and other cryptographic operations",
    )

    # WhatsApp
    whatsapp_webhook_verify_token: Optional[str] = Field(
        default=None, description="WhatsApp webhook verify token"
    )
    whatsapp_access_token: Optional[str] = Field(
        default=None, description="WhatsApp access token"
    )
    whatsapp_phone_number_id: Optional[str] = Field(
        default=None, description="WhatsApp phone number ID"
    )

    # Instagram
    instagram_access_token: Optional[str] = Field(
        default=None, description="Instagram access token"
    )

    # Facebook
    facebook_access_token: Optional[str] = Field(
        default=None, description="Facebook access token"
    )
    facebook_app_secret: Optional[str] = Field(
        default=None, description="Facebook app secret"
    )

    # Debounce Configuration
    debounce_default_seconds: int = Field(
        default=8, description="Default debounce time in seconds"
    )
    debounce_max_seconds: int = Field(
        default=15, description="Maximum debounce time in seconds"
    )
    debounce_adaptive_increment: int = Field(
        default=2, description="Adaptive increment for debounce time"
    )

    # SLA Configuration
    ack_deadline_seconds: int = Field(
        default=20, description="ACK deadline in seconds"
    )
    urgent_response_seconds: int = Field(
        default=300, description="Urgent response time in seconds"
    )


settings = Settings()
