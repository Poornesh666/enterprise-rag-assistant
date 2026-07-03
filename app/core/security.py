from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = settings.secret_key

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
     return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
     to_encode = data.copy()
     expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
     to_encode.update({"exp": expire})
     
     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=settings.algorithm)
     
     return encoded_jwt

def verify_access_token(token: str) -> Optional[dict]:
     try:
          payload = jwt.decode(token, SECRET_KEY, algorithms=[settings.algorithm])
          
          username = payload.get("sub")
          role = payload.get("role")
          
          if username is None or role is None:
               raise JWTError("Invalid token: missing username or role")
          
          return {"username": username, "role": role}
     except JWTError:
          return None
     
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[dict]:
     user = verify_access_token(token)
     
     if user is None:
          raise HTTPException(
               status_code=401,
               detail="Invalid or Expired token",
          )
          
     return user
