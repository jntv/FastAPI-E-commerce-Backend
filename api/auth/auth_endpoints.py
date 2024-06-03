from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from database import connection
from .models import User
# Replace 'secret_key' with a secure key for JWT generation
from jose import jwt, JWTError

from jose import JWTError
from datetime import datetime, timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/api/auth")

from sqlalchemy.orm import Session
from .models import User


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserBase(BaseModel):
    email: EmailStr
    password : str


class Token(BaseModel):
    access_token: str
    token_type: str
    
import secrets
JWT_SECRET_KEY = secrets.token_bytes(32)

def generate_access_token(email: EmailStr, expires_delta: Optional[timedelta] = None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_payload = {"exp": datetime.utcnow() + expires_delta, "email": email}
    return jwt.encode(token_payload, JWT_SECRET_KEY, algorithm="HS256")


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return payload["email"]
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


@router.post("/register")
async def register(user: CreateUser, db: Session = Depends(connection.get_db)):
    try:
        hashed_pass = pwd_context.hash(user.password)
        new_user = User(
                username    = user.username,
                email       = user.email,
                password    = hashed_pass
            )
        # Validate and save user to database
        db.add(new_user)
        db.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        if 'IntegrityError' in str(e):
            return {"message": "Duplicate values entered"}
        return {"message": str(e)}


@router.post("/login")
async def login(form: UserBase, db: Session = Depends(connection.get_db)):
    user =  db.query(User).filter(User.email == form.email).first()
    if not user:
        return {"message": "Invalid username or password"}
    
    if  not pwd_context.verify(secret=form.password, hash=user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    access_token = generate_access_token(user.email)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me")
async def get_current_user(db: Session = Depends(connection.get_db), current_user: EmailStr = Depends(verify_access_token)):
    user = db.query(User).filter(User.email == current_user).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return user
    
