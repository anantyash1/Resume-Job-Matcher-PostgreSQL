

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import sys
# import os

# # Add parent directory to path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# # Create FastAPI app
# app = FastAPI(
#     title="Resume Job Matcher API",
#     description="Classical ML-based resume to job matching system",
#     version="2.0.0"
# )

# # CRITICAL: CORS Configuration MUST come BEFORE routes
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins for testing
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Import and include routers AFTER CORS setup
# try:
#     from app.routes import auth, resume, jobs
#     app.include_router(auth.router)
#     app.include_router(resume.router)
#     app.include_router(jobs.router)
#     print("✓ Core routes loaded successfully")
# except ImportError as e:
#     print(f"⚠ Warning: Core routes import failed: {e}")

# # Try to import HR and applications routes (may not exist yet)
# try:
#     from app.routes import hr
#     app.include_router(hr.router)
#     print("✓ HR routes loaded successfully")
# except ImportError:
#     print("⚠ HR routes not available (this is OK if not implemented yet)")

# try:
#     from app.routes import applications
#     app.include_router(applications.router)
#     print("✓ Application routes loaded successfully")
# except ImportError:
#     print("⚠ Application routes not available (this is OK if not implemented yet)")

# # Initialize database
# @app.on_event("startup")
# async def startup_event():
#     """Initialize database on startup"""
#     try:
#         from app.database import init_db
#         init_db()
#         print("✓ Database initialized successfully")
#     except Exception as e:
#         print(f"⚠ Database initialization warning: {e}")

# # Root endpoint
# @app.get("/")
# async def root():
#     return {
#         "message": "Resume Job Matcher API",
#         "status": "running",
#         "version": "2.0.0",
#         "docs": "/docs"
#     }

# # Health check
# @app.get("/health")
# async def health_check():
#     return {"status": "healthy", "cors": "enabled"}

# # CORS test endpoint
# @app.get("/test-cors")
# async def test_cors():
#     return {"message": "CORS is working!", "origin": "allowed"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)





# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI(
#     title="Resume Job Matcher API",
#     version="2.0.0"
# )

# # CORS - Must be FIRST before any routes
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:3000",
#         "http://127.0.0.1:3000",
#         "http://localhost:3001",
#         "http://127.0.0.1:3001",
#     ],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
#     allow_headers=["*"],
# )

# # Import routes one by one with error reporting
# from app.routes import auth
# app.include_router(auth.router)
# print("✓ Auth routes loaded")

# from app.routes import resume
# app.include_router(resume.router)
# print("✓ Resume routes loaded")

# from app.routes import jobs
# app.include_router(jobs.router)
# print("✓ Jobs routes loaded")

# try:
#     from app.routes import hr
#     app.include_router(hr.router)
#     print("✓ HR routes loaded")
# except Exception as e:
#     print(f"✗ HR routes failed: {e}")

# try:
#     from app.routes import applications
#     app.include_router(applications.router)
#     print("✓ Applications routes loaded")
# except Exception as e:
#     print(f"✗ Applications routes failed: {e}")

# @app.on_event("startup")
# def startup_event():
#     try:
#         from app.database import init_db
#         init_db()
#         print("✓ Database ready")
#     except Exception as e:
#         print(f"✗ Database error: {e}")

# @app.get("/")
# def root():
#     return {"message": "Resume Job Matcher API", "status": "running"}

# @app.get("/health")
# def health():
#     return {"status": "healthy"}

# @app.get("/routes")
# def list_routes():
#     """Debug endpoint - shows all registered routes"""
#     routes = []
#     for route in app.routes:
#         if hasattr(route, 'methods'):
#             routes.append({
#                 "path": route.path,
#                 "methods": list(route.methods)
#             })
#     return routes








from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Resume Job Matcher API", version="2.0.0")

# CRITICAL: CORS MUST BE FIRST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Import routes AFTER CORS
from app.routes import auth, resume, jobs

app.include_router(auth.router)
print("✓ Auth routes loaded")

app.include_router(resume.router)
print("✓ Resume routes loaded")

app.include_router(jobs.router)
print("✓ Jobs routes loaded")

try:
    from app.routes import hr
    app.include_router(hr.router)
    print("✓ HR routes loaded")
except Exception as e:
    print(f"✗ HR routes error: {e}")

try:
    from app.routes import applications
    app.include_router(applications.router)
    print("✓ Application routes loaded")
except Exception as e:
    print(f"✗ Application routes error: {e}")

@app.on_event("startup")
def startup():
    from app.database import init_db
    init_db()
    print("✓ Database initialized")

@app.get("/")
def root():
    return {"message": "API Running", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}