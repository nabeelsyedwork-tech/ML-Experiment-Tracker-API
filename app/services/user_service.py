from sqlalchemy.orm import Session
from app.db.models import User

def fetch_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
