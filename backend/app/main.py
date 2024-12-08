from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from .core.config import settings
from .api.v1 import api_router

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="StickerMania API - A comprehensive soccer collectibles management platform",
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    # Configure trailing slash behavior
    redirect_slashes=True
)

# Set custom OpenAPI schema
app.openapi = custom_openapi

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": "Welcome to StickerMania API",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi_json": f"{settings.API_V1_STR}/openapi.json"
        },
        "version": settings.VERSION,
        "status": "operational"
    }

# Startup event to initialize database connection
@app.on_event("startup")
async def startup_event():
    # We can add database connection initialization here
    pass

# Shutdown event to close database connection
@app.on_event("shutdown")
async def shutdown_event():
    # We can add database connection cleanup here
    pass
