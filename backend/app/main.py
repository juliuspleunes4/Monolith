"""FastAPI application entry point."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.routers import chat, models, conversations

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting Monolith backend...")
    # TODO: Initialize LLM engine on startup
    # TODO: Load available models from MODELS_DIR
    yield
    logger.info("Shutting down Monolith backend...")
    # TODO: Cleanup and unload models


app = FastAPI(
    title="Monolith API",
    description="Local LLM chat interface API",
    version="0.1.0",
    lifespan=lifespan
)

# CORS configuration
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3001")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:3000"],  # Support both ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(models.router, prefix="/api/v1", tags=["models"])
app.include_router(conversations.router, prefix="/api/v1", tags=["conversations"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Monolith",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
