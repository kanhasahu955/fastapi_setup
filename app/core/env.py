from functools import lru_cache
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings,SettingsConfigDict
from pathlib import Path

_ENV_PATH = Path(__file__).resolve().parent.parent

class Settiings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_PATH / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # APP
    app_name: str = Field(default="FastAPI Practice")
    debug: bool = Field(default=True)

    # DATABASE
    database_url: str = Field(
        default="sqlite:///./test.db"
    )

    # JWT
    jwt_secret_key: str = "supersecretkey123"    
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000"]
    )
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )
    cors_allow_headers: List[str] = Field(
        default=["*"]
    )

    # RATE LIMIT
    rate_limit: str = "100/minute"


@lru_cache
def get_settings()->Settiings:
    return Settiings()