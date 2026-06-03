from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.services.user_service import fetch_user
from app.db.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

async def get_current_user(KEY:str, ALGORITHM:str, token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,KEY,algorithms=[ALGORITHM])
        username = payload.get('sub')
        userid = payload.get('userid')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = fetch_user(db,username=username)
    if user is None:
        raise credentials_exception
    return user