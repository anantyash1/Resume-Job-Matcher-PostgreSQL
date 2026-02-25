from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import init_db
from .routes import applications, auth, hr, jobs, resume

settings = get_settings()

app = FastAPI(
    title="Resume Job Matcher API",
    version="2.0.0",
)

# Keep CORS origins configurable via env (FRONTEND_URLS / FRONTEND_URL).
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Routers already define their own prefixes (e.g. /auth, /hr, /resume).
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(jobs.router)
app.include_router(hr.router)
app.include_router(applications.router)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/")
def root():
    return {
        "message": "Resume Job Matcher API",
        "status": "running",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/test-cors")
def test_cors():
    return {"message": "CORS is working"}
