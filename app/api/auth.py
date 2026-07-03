# =========================================================
# Authentication Endpoints
# =========================================================

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import verify_password, create_access_token, get_current_user
from app.data.users import users_db

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate a user and return a JWT access token.
    """

    user = users_db.get(form_data.username)

    if not user or not verify_password(
        form_data.password,
        user["password"],
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password.",
        )

    token = create_access_token(
        {
            "sub": form_data.username,
            "role": user["role"],
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user["role"],
    }


@router.get("/test")
def test(current_user: dict = Depends(get_current_user)):
    """
    Test endpoint for verifying JWT authentication.
    """

    return {
        "message": f"Hello {current_user['username']}!",
        "role": current_user["role"],
    }