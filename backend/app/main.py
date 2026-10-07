"""
RetailPulse AI — Main FastAPI Application
Serves the React frontend as static files AND the REST API on a single port.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import logging

from backend.app.core.config import settings
from backend.app.api.v1.router import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("retailpulse")

# Resolve path to the compiled React app
_HERE = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIST = os.path.normpath(os.path.join(_HERE, "..", "..", "frontend", "dist"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("RetailPulse AI backend starting up...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Database URL: {settings.DATABASE_URL}")
    if os.path.exists(FRONTEND_DIST):
        logger.info(f"Serving React frontend from: {FRONTEND_DIST}")
    else:
        logger.warning(
            f"Frontend build not found at {FRONTEND_DIST}. "
            "Run: cd frontend && npm run build"
        )
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

# CORS Middleware — still useful for dev mode where Vite runs separately
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Global Exception Handler ─────────────────────────────────────────────────
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


# ─── API Routes (registered FIRST so /api/** always wins) ────────────────────
app.include_router(api_router, prefix="/api")
app.include_router(api_router, prefix="/api/v1")


# ─── Serve React SPA (registered AFTER /api routes) ─────────────────────────
if os.path.exists(FRONTEND_DIST):
    # Mount static assets (JS, CSS, images) — exact paths like /assets/index.js
    app.mount(
        "/assets",
        StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")),
        name="frontend-assets"
    )

    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon():
        favicon_path = os.path.join(FRONTEND_DIST, "favicon.ico")
        if os.path.exists(favicon_path):
            return FileResponse(favicon_path)
        return JSONResponse(status_code=204, content={})

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_react_app(full_path: str):
        """
        Catch-all: serve an existing static file if it exists,
        otherwise fall back to index.html so React Router handles the path.
        """
        # Reserved paths for FastAPI documentation and API routes
        reserved = ("api", "docs", "redoc", "openapi.json", "swagger.json")
        if any(full_path.startswith(r) for r in reserved):
            raise HTTPException(status_code=404)
        target = os.path.join(FRONTEND_DIST, full_path)
        if os.path.exists(target) and os.path.isfile(target):
            return FileResponse(target)
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))

else:
    @app.get("/", include_in_schema=False)
    def root():
        return {
            "name": "RetailPulse AI API",
            "status": "operational",
            "note": "React frontend not built. Run: cd frontend && npm run build",
            "documentation": "/docs",
            "api_v1": "/api"
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG
    )
