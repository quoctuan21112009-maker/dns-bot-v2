from pydantic_settings import BaseSettings
from typing import List
import os
from datetime import timedelta

class Settings(BaseSettings):
    """Application settings"""
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://user:password@localhost:5432/dnsbot"
    )
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-me")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost",
        "http://127.0.0.1",
    ]
    
    # File Upload
    UPLOAD_FOLDER: str = "uploads"
    OUTPUT_FOLDER: str = "outputs"
    MAX_UPLOAD_SIZE: int = 64 * 1024 * 1024  # 64MB
    ALLOWED_EXTENSIONS: set = {
        "txt", "md", "csv", "json", "xml",
        "png", "jpg", "jpeg", "gif", "webp",
        "mp4", "webm", "ogg",
        "py", "js", "html", "css", "java", "cpp", "c",
        "pdf", "doc", "docx"
    }
    
    # AI Providers
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    
    DEFAULT_AI_PROVIDER: str = "groq"
    DEFAULT_AI_MODEL: str = "llama-3.1-8b-instant"
    
    # External APIs
    GITHUB_API_TOKEN: str = os.getenv("GITHUB_API_TOKEN", "")
    JUDGE0_API_KEY: str = os.getenv("JUDGE0_API_KEY", "")
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE: str = os.getenv("TWILIO_PHONE", "")
    
    # WebSocket
    WEBSOCKET_PING_INTERVAL: int = 30
    WEBSOCKET_PING_TIMEOUT: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()