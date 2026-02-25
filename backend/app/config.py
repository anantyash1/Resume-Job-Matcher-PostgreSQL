from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Render exposes DATABASE_URL automatically.
    DATABASE_URL: str = "postgresql://resume_user:secure_password_123@localhost:5432/resume_matcher"

    # JWT
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200

    # Environment
    ENVIRONMENT: str = "development"

    # CORS
    FRONTEND_URLS: str = "http://localhost:3000,http://127.0.0.1:3000"
    FRONTEND_URL: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def database_url_fixed(self) -> str:
        """Render may still provide postgres://; SQLAlchemy expects postgresql://."""
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql://", 1)
        return url

    @property
    def cors_origins(self) -> List[str]:
        origins = []

        if self.FRONTEND_URLS:
            origins.extend(
                origin.strip().rstrip("/")
                for origin in self.FRONTEND_URLS.split(",")
                if origin.strip()
            )

        if self.FRONTEND_URL:
            origins.append(self.FRONTEND_URL.strip().rstrip("/"))

        # Keep local dev URLs available.
        origins.extend(
            [
                "http://localhost:3000",
                "http://127.0.0.1:3000",
                "http://localhost:3001",
                "http://127.0.0.1:3001",
            ]
        )

        deduped = []
        seen = set()
        for origin in origins:
            if origin not in seen:
                seen.add(origin)
                deduped.append(origin)
        return deduped


@lru_cache()
def get_settings() -> Settings:
    return Settings()
