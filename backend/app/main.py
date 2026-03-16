from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
from app.config import settings
from app.database import engine, Base
from app import api

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    # Startup
    logger.info("🚀 Starting DNS Bot v2...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    logger.info("🛑 Shutting down DNS Bot v2...")

# Create FastAPI app
app = FastAPI(
    title="DNS Bot API",
    description="Intelligent AI Agent for Class 11A1",
    version="2.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api.auth.router)
app.include_router(api.chat.router)
app.include_router(api.code.router)
app.include_router(api.ai.router)
app.include_router(api.github.router)
app.include_router(api.tasks.router)
app.include_router(api.media.router)
app.include_router(api.video.router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "DNS Bot v2 API",
        "version": "2.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL
    )