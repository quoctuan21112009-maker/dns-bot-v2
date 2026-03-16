from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr
from app.database import get_db_session
from app.models.user import User
from app.security.jwt import create_access_token, verify_password, hash_password
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str | None = None
    fullname: str | None = None

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

@router.post("/register", response_model=dict)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db_session)
):
    """Register new user"""
    
    # Check if user exists
    from sqlalchemy import select
    existing = await db.execute(
        select(User).where(User.username == request.username)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
    
    # Create new user
    user = User(
        username=request.username,
        email=request.email,
        fullname=request.fullname,
        password_hash=hash_password(request.password)
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    logger.info(f"✅ User {request.username} registered")
    
    return {
        "success": True,
        "message": "Registration successful",
        "user_id": user.id
    }

@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db_session)
):
    """Login user"""
    
    from sqlalchemy import select
    result = await db.execute(
        select(User).where(User.username == request.username)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Update last login
    from datetime import datetime
    user.last_login = datetime.utcnow()
    db.add(user)
    await db.commit()
    
    # Generate token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    logger.info(f"✅ User {user.username} logged in")
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user.id,
            "username": user.username,
            "fullname": user.fullname,
            "email": user.email,
            "role": user.role
        }
    )

@router.get("/me")
async def get_current_user(
    current_user: User = Depends(lambda: None),
):
    """Get current user info"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "fullname": current_user.fullname,
        "email": current_user.email,
        "role": current_user.role,
        "ai_provider": current_user.ai_provider,
        "ai_model": current_user.ai_model
    }