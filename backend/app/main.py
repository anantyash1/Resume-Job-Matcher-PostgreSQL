
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI(title="Resume Job Matcher API", version="2.0.0")

# # CRITICAL: CORS MUST BE FIRST
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["*"]
# )

# # Import routes AFTER CORS
# from app.routes import auth, resume, jobs

# app.include_router(auth.router)
# print("✓ Auth routes loaded")

# app.include_router(resume.router)
# print("✓ Resume routes loaded")

# app.include_router(jobs.router)
# print("✓ Jobs routes loaded")

# try:
#     from app.routes import hr
#     app.include_router(hr.router)
#     print("✓ HR routes loaded")
# except Exception as e:
#     print(f"✗ HR routes error: {e}")

# try:
#     from app.routes import applications
#     app.include_router(applications.router)
#     print("✓ Application routes loaded")
# except Exception as e:
#     print(f"✗ Application routes error: {e}")

# @app.on_event("startup")
# def startup():
#     from app.database import init_db
#     init_db()
#     print("✓ Database initialized")

# @app.get("/")
# def root():
#     return {"message": "API Running", "status": "ok"}

# @app.get("/health")
# def health():
#     return {"status": "healthy"}


####################################
# # For Vercel serverless deployment
# app = your_fastapi_app_instance  # make sure you have app defined

# # This is the handler Vercel will call
# def handler(request):
#     return app(request)
##############################

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from .config import get_settings

# settings = get_settings()

# app = FastAPI(
#     title="Resume Job Matcher API",
#     version="2.0.0",
#     docs_url="/docs",
#     redoc_url="/redoc"
# )

# # CORS - Allow frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.FRONTEND_URLS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["*"]
# )

# # Import routes
# from app.routes import auth, resume, jobs

# app.include_router(auth.router)
# print("✓ Auth routes loaded")

# app.include_router(resume.router)
# print("✓ Resume routes loaded")

# app.include_router(jobs.router)
# print("✓ Jobs routes loaded")

# try:
#     from app.routes import hr
#     app.include_router(hr.router)
#     print("✓ HR routes loaded")
# except Exception as e:
#     print(f"✗ HR routes error: {e}")

# try:
#     from app.routes import applications
#     app.include_router(applications.router)
#     print("✓ Application routes loaded")
# except Exception as e:
#     print(f"✗ Application routes error: {e}")


# @app.on_event("startup")
# def startup():
#     """Run on application startup"""
#     print(f"Starting in {settings.ENVIRONMENT} mode...")
#     print(f"Allowed origins: {settings.FRONTEND_URLS}")


# @app.get("/")
# def root():
#     return {
#         "message": "Resume Job Matcher API",
#         "status": "running",
#         "environment": settings.ENVIRONMENT,
#         "version": "2.0.0"
#     }


# @app.get("/health")
# def health():
#     """Health check endpoint"""
#     return {"status": "healthy"}


# @app.get("/api-info")
# def api_info():
#     """API information"""
#     return {
#         "api": "Resume Job Matcher",
#         "docs": "/docs",
#         "health": "/health"
#     }





# #main.py

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from .config import get_settings
# import os

# settings = get_settings()

# app = FastAPI(
#     title="Resume Job Matcher API",
#     version="2.0.0"
# )

# # CORS - Allow all origins (can restrict later)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all for now
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["*"]
# )

# # Import routes
# from app.routes import auth, resume, jobs

# app.include_router(auth.router)
# print("✓ Auth routes loaded")

# app.include_router(resume.router)
# print("✓ Resume routes loaded")

# app.include_router(jobs.router)
# print("✓ Jobs routes loaded")

# try:
#     from app.routes import hr
#     app.include_router(hr.router)
#     print("✓ HR routes loaded")
# except Exception as e:
#     print(f"✗ HR routes error: {e}")

# try:
#     from app.routes import applications
#     app.include_router(applications.router)
#     print("✓ Application routes loaded")
# except Exception as e:
#     print(f"✗ Application routes error: {e}")


# @app.on_event("startup")
# def startup():
#     print(f"Starting in {settings.ENVIRONMENT} mode")


# @app.get("/")
# def root():
#     return {
#         "message": "Resume Job Matcher API",
#         "status": "running",
#         "environment": settings.ENVIRONMENT
#     }


# @app.get("/health")
# def health():
#     return {"status": "healthy"}



# from backend.app.database import init_db
from .database import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
import os

settings = get_settings()

app = FastAPI(
    title="Resume Job Matcher API",
    version="2.0.0"
)

# CORS - Configure properly for your domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://resumejobmatcher.onrender.com",  # Your frontend
        "https://naukrilite.onrender.com",        # Your backend (self)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Import all routes
from app.routes import auth, resume, jobs, hr, applications

# Register all routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
print("✓ Auth routes loaded")

app.include_router(resume.router, prefix="/resume", tags=["resume"])
print("✓ Resume routes loaded")

app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
print("✓ Jobs routes loaded")

app.include_router(hr.router, prefix="/hr", tags=["hr"])
print("✓ HR routes loaded")

app.include_router(applications.router, prefix="/applications", tags=["applications"])
print("✓ Application routes loaded")

@app.on_event("startup")
def startup():
    print(f"Starting in {settings.ENVIRONMENT} mode")
    print(f"Database URL: {settings.database_url_fixed[:20]}...")
    init_db()  # Ensure database is initialized on startup  
    print("✓ Database tables created/verified")

@app.get("/")
def root():
    return {
        "message": "Resume Job Matcher API",
        "status": "running",
        "environment": settings.ENVIRONMENT
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/test-cors")
def test_cors():
    return {"message": "CORS is working!"}