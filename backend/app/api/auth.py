from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, Any
from backend.app.schemas.auth import UserLogin, Token, UserResponse
from backend.app.core.database import get_db
from backend.app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db = Depends(get_db)):
    users_coll = db.get_collection("users")
    user = await users_coll.find_one({"email": credentials.email.strip().lower()})
    
    if not user or not verify_password(credentials.password, user.get("hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid analyst email or credentials. Please check your credentials.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user_res = UserResponse(
        id=user.get("id", user.get("_id", "")),
        email=user["email"],
        full_name=user.get("full_name", "SOC Analyst"),
        role=user.get("role", "Senior Analyst"),
        department=user.get("department", "Security Operations")
    )

    access_token = create_access_token(data={"sub": user["email"], "role": user.get("role")})

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_res
    )
