from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from ..models import UserCreate, UserLogin, Token, User, UserResponse
from ..auth import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from ..database import get_collection


router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    users_collection = await get_collection("users")
    
    # Check if user already exists
    existing_user = await users_collection.find_one({
        "$or": [
            {"email": user_data.email},
            {"username": user_data.username}
        ]
    })
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )
    
    # Hash password and create user
    hashed_password = get_password_hash(user_data.password)
    
    user = User(
        email=user_data.email,
        username=user_data.username,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
        phone=user_data.phone,
        hashed_password=hashed_password,
        is_verified=True  # Auto-verify for now
    )
    
    # Insert into database
    user_dict = user.dict()
    await users_collection.insert_one(user_dict)
    
    # Return user response
    return UserResponse(**user_dict)


@router.post("/login", response_model=Token)
async def login_user(user_data: UserLogin):
    """Login user and return JWT token"""
    users_collection = await get_collection("users")
    
    # Find user
    user = await users_collection.find_one({"username": user_data.username})
    
    if not user or not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_login": datetime.now()}}
    )
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, 
        expires_delta=access_token_expires
    )
    
    # Prepare user response
    user_response = UserResponse(
        id=user["id"],
        email=user["email"],
        username=user["username"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        role=user["role"],
        phone=user.get("phone"),
        is_verified=user["is_verified"],
        last_login=user.get("last_login"),
        created_at=user["created_at"]
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # in seconds
        user=user_response
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(security)):
    """Get current user information"""
    users_collection = await get_collection("users")
    
    # Extract token
    token = current_user.credentials
    # For now, return mock data
    # In a real implementation, you'd decode the token and fetch user data
    return UserResponse(
        id="mock-id",
        email="user@example.com",
        username="current_user",
        first_name="Current",
        last_name="User",
        role="doctor",
        is_verified=True,
        created_at=datetime.now()
    )