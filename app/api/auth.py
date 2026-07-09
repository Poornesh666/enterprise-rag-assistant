# =========================================================
# Authentication Endpoints
# =========================================================

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import verify_password, create_access_token, get_current_user
from app.core.logging import logger
from app.schemas.responses import LoginResponse, TestResponse

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.user import get_user_by_username

from app.schemas.register import RegisterRequest
from app.crud.user import create_user, get_user_by_username

router = APIRouter()

@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):

    existing_user = get_user_by_username(
        db,
        request.username,
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Username already exists.",
        )

    user = create_user(
        db=db,
        username=request.username,
        password=request.password,
        role=request.role,
    )

    return {
        "message": "User registered successfully.",
        "username": user.username,
        "role": user.role,
    }

@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate a user and return a JWT access token.
    """

    user = get_user_by_username(
        db,
        form_data.username,
    )    

    if not user or not verify_password(
        form_data.password,
        user.password,
    ):
        logger.warning(f"Failed login attempt for '{form_data.username}'.")
        
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password.",
        )

    token = create_access_token(
        {
            "sub": form_data.username,
            "role": user.role,
        }
    )

    logger.info(f"User '{form_data.username}' logged in successfully.")

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
    }



@router.get("/test", response_model=TestResponse)
def test(current_user: dict = Depends(get_current_user)):
    """
    Test endpoint for verifying JWT authentication.
    """

    return {
        "message": f"Hello {current_user['username']}!",
        "role": current_user["role"],
    }