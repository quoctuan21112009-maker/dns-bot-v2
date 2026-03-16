from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    phone = Column(String(20), unique=True, index=True, nullable=True)
    fullname = Column(String(100), nullable=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(255), nullable=True)
    role = Column(String(20), default="student")  # student, teacher, admin
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # AI Config
    ai_provider = Column(String(50), default="groq")
    ai_model = Column(String(100), default="llama-3.1-8b-instant")
    ai_api_key = Column(String(500), nullable=True)
    
    # GitHub
    github_token = Column(String(500), nullable=True)
    github_username = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<User {self.username}>"