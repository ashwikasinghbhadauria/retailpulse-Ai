"""
RetailPulse AI — Main FastAPI Application
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from backend.app.core.config import settings
from backend.app.api.v1.router import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("retailpulse")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("RetailPulse AI backend starting up...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Database URL: {settings.DATABASE_URL}")
    yield
    logger.info("RetailPulse AI backend shutting down...")

app = FastAPI(
    title="RetailPulse AI — Autonomous Retail Intelligence API",
    description=(
        "Enterprise-grade AI-powered retail business intelligence and predictive analytics platform. "
        "Delivers descriptive, diagnostic, predictive, and prescriptive analytics alongside a tool-grounded AI Business Analyst."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred during analytics computation. Please verify parameters or retry.",
            "path": request.url.path
        }
    )

# Include API Router under /api and /api/v1
app.include_router(api_router, prefix="/api")
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "name": "RetailPulse AI",
        "status": "operational",
        "documentation": "/docs",
        "api_v1": "/api"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=settings.DEBUG)
