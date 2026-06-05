from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.security import (create_access_token, verify_password, get_password_hash)
from app.services.user_service import fetch_user
from app.db.database import get_db
from app.schemas.user import (UserCreate, UserOut)
from app.dependencies.auth import get_current_user
from app.db.models import User
from app.core.config import settings
from app.core.logger import logger

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
def create_user(user: UserCreate,db: Session = Depends(get_db)):
   db_user = fetch_user(db, username=user.username)
   if db_user:
        logger.warning(f"Username {user.username} already registered")
        raise HTTPException(status_code=400, detail="Username already registered")
   hashed_password = get_password_hash(user.password)
   db_user = User(username=user.username, password=hashed_password)
   db.add(db_user)
   db.commit()
   db.refresh(db_user)
   logger.info(f"User {user.username} registered")
   return {
       "Message":f"User {user.username} registered",
        "UserID":db_user.userid      
    }


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = fetch_user(db, username=form_data.username)
    if not user or not verify_password(form_data.password,user.password):
        logger.warning(f"Failed login attempt username = {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":user.username, "userid": user.userid}, expire_delta=access_token_expires,KEY=settings.SECRET_KEY,ALGORITHM=settings.ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user