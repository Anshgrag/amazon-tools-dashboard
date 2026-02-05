from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, verify_token
from app.core.config import settings
from app.schemas.auth import UserCreate, UserLogin, UserResponse, TokenResponse
from app.models.auth import User
from app.core.exceptions import AuthenticationError, ValidationError

router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user"""
    # Check if user already exists
    existing_user = await User.get_by_email(db, user_data.email)
    if existing_user:
        raise ValidationError("Email already registered")
    
    # Create new user
    user = await User.create(db, user_data)
    
    return UserResponse.from_orm(user)


@router.post("/login", response_model=TokenResponse)
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return tokens"""
    # Authenticate user
    user = await User.authenticate(db, user_data.email, user_data.password)
    if not user:
        raise AuthenticationError("Invalid credentials")
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token using refresh token"""
    # Verify refresh token
    email = verify_token(refresh_token, token_type="refresh")
    
    # Check if user still exists
    user = await User.get_by_email(db, email)
    if not user:
        raise AuthenticationError("User not found")
    
    # Create new access token
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,  # Return same refresh token
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile"""
    return UserResponse.from_orm(current_user)


async def get_current_user(
    credentials: str = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    email = verify_token(token, token_type="access")
    
    user = await User.get_by_email(db, email)
    if not user:
        raise AuthenticationError("User not found")
    
    return user