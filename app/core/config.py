import secrets, os
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):

    REDIS_DB = "3decision_data"
    API_V3_STR: str = "/api/v3"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = "local"
    SERVER_HOST: AnyHttpUrl = "http://local.api.discngine.com"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://local.api.discngine.com",
        "http://local.api.discngine.com:5555",
        "http://local.api.discngine.com:3000"
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "3decision Backend"
    PROJECT_PATH = os.getcwd()
    PROCESS_ROUTES: dict = {"app.worker.process": "process-structure"}
    SENTRY_DSN: Optional[HttpUrl] = None

    class Config:
        case_sensitive = True


settings = Settings()
