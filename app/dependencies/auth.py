from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.services.user_service import fetch_user
from app.db.database import get_db
from app.core.logger import logger
from app.core.config import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

async def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        username = payload.get('sub')
        userid = payload.get('userid')
        if username is None:
            logger.error("Could not validate credentials")
            raise credentials_exception
    except JWTError:
        logger.warning("Invalid JWT token")
        raise credentials_exception
    
    user = fetch_user(db,username=username)
    if user is None:
        logger.warning(f"User {user} not found in database")
        raise credentials_exception
    return user