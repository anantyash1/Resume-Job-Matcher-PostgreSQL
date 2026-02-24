# # from pydantic_settings import BaseSettings
# # from functools import lru_cache


# # class Settings(BaseSettings):
# #     # Database
# #     DATABASE_URL: str = "postgresql://resume_user:secure_password_123@localhost:5432/resume_matcher"
    
# #     # JWT
# #     SECRET_KEY: str = "your-secret-key-here"
# #     ALGORITHM: str = "HS256"
# #     ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200
    
# #     # Environment
# #     ENVIRONMENT: str = "development"
    
# #     class Config:
# #         env_file = ".env"
# #         case_sensitive = True


# # @lru_cache()
# # def get_settings():
# #     return Settings()


# from pydantic_settings import BaseSettings
# from functools import lru_cache
# import os


# class Settings(BaseSettings):
#     # Database - Render provides DATABASE_URL automatically
#     DATABASE_URL: str = os.getenv(
#         "DATABASE_URL",
#         "postgresql://resume_user:secure_password_123@localhost:5432/resume_matcher"
#     )
    
#     # Fix Render's postgres:// to postgresql://
#     @property
#     def database_url_fixed(self):
#         url = self.DATABASE_URL
#         if url and url.startswith("postgres://"):
#             url = url.replace("postgres://", "postgresql://", 1)
#         return url
    
#     # JWT
#     SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200
    
#     # Environment
#     ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
#     # CORS - Frontend URLs
#     FRONTEND_URLS: list = [
#         "http://localhost:3000",
#         "http://127.0.0.1:3000",
#     ]
    
#     def add_frontend_url(self, url: str):
#         if url and url not in self.FRONTEND_URLS:
#             self.FRONTEND_URLS.append(url)
    
#     class Config:
#         env_file = ".env"
#         case_sensitive = True


# @lru_cache()
# def get_settings():
#     settings = Settings()
    
#     # Add production frontend URL if provided
#     frontend_url = os.getenv("FRONTEND_URL")
#     if frontend_url:
#         settings.add_frontend_url(frontend_url)
#         # Also add without trailing slash
#         settings.add_frontend_url(frontend_url.rstrip('/'))
    
#     return settings


from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    # Database - Render provides this automatically
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://resume_user:secure_password_123@localhost:5432/resume_matcher"
    )
    
    # Fix Render's postgres:// to postgresql://
    @property
    def database_url_fixed(self):
        url = self.DATABASE_URL
        if url and url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()